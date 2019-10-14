CREATE USER 'monitor'@'%' IDENTIFIED BY 'monitorpassword';
GRANT SELECT on sys.* to 'monitor'@'%';
FLUSH PRIVILEGES;

CREATE USER 'lsappuser'@'%' IDENTIFIED BY 'lsapppassword';
GRANT ALL PRIVILEGES on lsapp.* to 'lsappuser'@'%';
FLUSH PRIVILEGES;