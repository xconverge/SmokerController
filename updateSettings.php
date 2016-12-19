<?php
if ($_GET) {
    $fanOn = $_GET['fanOn'];
    $fanOff = $_GET['fanOff'];
    $time = $_GET['time'];
} else {
    $fanOn = $argv[1];
    $fanOff = $argv[2];
    $time = $argv[3];
}
/*
echo $fanOn, $fanOff, $time;
*/
exec("sqlite3 -line /var/www/templog.db 'UPDATE settings SET fanonthreshold=$fanOn, fanoffthreshold=$fanOff, timetodisplay=$time;'")

?>