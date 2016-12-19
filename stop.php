<?php
exec("sqlite3 -line /var/www/templog.db 'UPDATE settings SET isrunning=0'")
?>
