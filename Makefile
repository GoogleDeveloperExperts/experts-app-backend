default: dev

deploy:
	gcloud preview app deploy --project elite-firefly-737 --version 5 app.yaml

dev:
	dev_appserver.py .

chrome_dev:
	/Applications/Google\ Chrome\ Canary.app/Contents/MacOS/Google\ Chrome\ Canary --user-data-dir=~/test --unsafely-treat-insecure-origin-as-secure=http://localhost:8080