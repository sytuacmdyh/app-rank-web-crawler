<?php
/**
 * Created by PhpStorm.
 * User: dyh
 * Date: 17-12-7
 * Time: 下午11:59
 */

require_once __DIR__ . '/../vendor/autoload.php';

use League\Csv\Writer;
use \GuzzleHttp\Client;

function getRankList(Client $client, $date, $token)
{
    $r = $client->request('POST', 'http://fsight.qq.com/GameListAjax', [
        'headers'     => [
            'X-CSRF-TOKEN'  => $token,
            'X-BEE-COUNTRY' => 0,
        ],
//    'debug' => true,
        'form_params' => [
            'listCat'   => '3',
            'listType'  => '0',
            'rankRange' => '1',
            'listDate'  => $date
        ]
    ]);

    $body = json_decode($r->getBody()->getContents(), true);

    return $body;
}

$rankCsv = Writer::createFromPath('data/rank.csv', 'w');
$appCsv  = Writer::createFromPath('data/app.csv', 'w');

$client = new Client(['cookies' => true]);
$r      = $client->request('GET', 'http://fsight.qq.com/GameList?type=hotRank');

//var_dump($r->getHeaders());

$headers      = $r->getHeaders();
$wetest_token = $headers['Set-Cookie'][3];
$wetest_token = explode('=', $wetest_token)[1];
$wetest_token = explode(';', $wetest_token)[0];
$wetest_token = urldecode($wetest_token);

var_dump($wetest_token);


$app = [];

$curDate = "2017-11-01";
$endDate = "2017-12-01";
while ($curDate != $endDate) {

    $ranks = getRankList($client, $curDate, $wetest_token)['ret']['ranks'];
    $val = [];
    foreach ($ranks as $rank) {
        $app[$rank['entityId']] = $rank['game_name'];
        $val[]= $rank['entityId'];
    }
    $rankCsv->insertOne($val);

    echo "$curDate\n";
    $curDate = date('Y-m-d', strtotime($curDate . " +1 day"));
}

foreach ($app as $key => $value) {
    $appCsv->insertOne([$key, $value]);
}


