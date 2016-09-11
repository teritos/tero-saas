Tero Modules Explanation
========================

bot
	- All related code to bots that notify users goes here
core
	- Mostly database models and code that is common to other modules
fixtures
	- Sample data
ftpd
	- FTPd server that receives IP Webcam's (or other sensors) data
	  by ftp and notify the user alarm
saas
	- Will be used if you want to deploy the project as
	  Software As a Service. Right now it gives you a django admin where
	  you can (hostile) manage alarms, users, etc.
