<?php
exec("sqlite3 -line /var/www/templog.db 'delete FROM temps;'")
?>
