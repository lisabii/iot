<?php
/**
 * Created by PhpStorm.
 * User: khalil
 * Date: 9/20/2018
 * Time: 7:50 PM
 */

require 'C:\Users\khalil\vendor\autoload.php';

date_default_timezone_set('UTC');

use Aws\DynamoDb\Exception\DynamoDbException;
use Aws\DynamoDb\Marshaler;

$sdk = new Aws\Sdk([
    'region'   => 'us-west-2',
    'version'  => 'latest'
]);

$dynamodb = $sdk->createDynamoDb();
$marshaler = new Marshaler();

$tableName = 'Iot';

$params = [
    'TableName' => $tableName
];

try {
    $result = $dynamodb->scan($params);
    echo "<h3> List of Records:</h3>";
    echo "<ul>";
    foreach ($result["Items"] as $i){
        $record = $marshaler -> unmarshalItem($i);
        echo "<li><p>Device ID:".$record["deviceId"].", Time:".$record["time"].", Device Name:".$record["deviceName"].", Download Photo:<a href=\"".$record["photoUrl"]."\">Photo </a></p></li>";
    }
    echo "</ul>";

} catch (DynamoDbException $e) {
    echo "Unable to get item:\n";
    echo $e->getMessage() . "\n";
}

?>