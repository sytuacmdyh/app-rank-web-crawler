<?php
/**
 * Created by PhpStorm.
 * User: dyh
 * Date: 17-12-7
 * Time: 下午11:59
 */

require_once __DIR__ . '/../vendor/autoload.php';

use League\Csv\Writer;
use GuzzleHttp\Client;

function getRankList(Client $client, $date, $token, $rankRange = 1)
{
    $r = $client->request('POST', 'http://fsight.qq.com/GameListAjax', [
        'headers'     => [
            'X-CSRF-TOKEN'  => $token,
            'X-BEE-COUNTRY' => 0,
        ],
//    'debug' => true,
        'form_params' => [
            'listCat'   => '3',//1：免费榜 2：付费榜 3：畅销榜
            'listType'  => '0',//有点多， 0为总榜
            'rankRange' => $rankRange,//区间 1：1~30 2:31~200 3:201~600 。。。 最大为8:1201~1391
            'listDate'  => $date
        ]
    ]);

    $body = json_decode($r->getBody()->getContents(), true);

    return $body['ret']['ranks'];
}

//获取某一天，排行榜的前200名
function getTop200(Client $client, $date, $token)
{
    $r1_30   = getRankList($client, $date, $token, 1);
    $r31_200 = getRankList($client, $date, $token, 2);
    return array_merge($r1_30, $r31_200);
}

//获取token（不用纠结这一段）
$client       = new Client(['cookies' => true]);
$r            = $client->request('GET', 'http://fsight.qq.com/GameList?type=hotRank');
$headers      = $r->getHeaders();
$wetest_token = $headers['Set-Cookie'][3];
$wetest_token = explode('=', $wetest_token)[1];
$wetest_token = explode(';', $wetest_token)[0];
$wetest_token = urldecode($wetest_token);

//起止时间
$curDate = "2017-11-01";
$endDate = "2017-12-01";

//创建csv文件
$rankCsv = Writer::createFromPath("data/{$curDate}_{$endDate}_rank.csv", 'w');
$appCsv  = Writer::createFromPath("data/{$curDate}_{$endDate}_app.csv", 'w');

//保存所有应用信息
$app = [];

//保存排名
while ($curDate != $endDate) {

    $ranks = getTop200($client, $curDate, $wetest_token);
    $val   = [];
    foreach ($ranks as $rank) {
        $app[$rank['entityId']] = $rank['game_name'];
        $val[]                  = $rank['entityId'];
    }
    $rankCsv->insertOne($val);

    echo "$curDate\n";
    $curDate = date('Y-m-d', strtotime($curDate . " +1 day"));
}

//保存应用信息
foreach ($app as $key => $value) {
    $appCsv->insertOne([$key, $value]);
}
