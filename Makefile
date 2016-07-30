default: dev

deploy:
	gcloud preview app deploy --project elite-firefly-737 --version 5 app.yaml

dev:
	dev_appserver.py .

chrome_dev:
	/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --user-data-dir=/Users/nawaid/Documents/test --unsafely-treat-insecure-origin-as-secure=http://localhost:8080