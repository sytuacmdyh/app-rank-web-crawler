<?php
/**
 * Created by PhpStorm.
 * User: dyh
 * Date: 17-12-8
 * Time: 上午12:01
 */

require_once __DIR__.'/../vendor/autoload.php';

use League\Csv\Writer;

//we create the CSV into memory
$csv = Writer::createFromPath('user.csv','w');

//we insert the CSV header
$csv->insertOne(['firstname', 'lastname', 'email']);

// The PDOStatement Object implements the Traversable Interface
// that's why Writer::insertAll can directly insert
// the data into the CSV
$csv->insertAll([['123','223']]);

// Because you are providing the filename you don't have to
// set the HTTP headers Writer::output can
// directly set them for you
// The file is downloadable
//$csv->output('users.csv');