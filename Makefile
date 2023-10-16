build:
	rm -rf my_deployment_package*;
	pip install --target ./package -r requirements.txt;
	cd package/;
	zip -r ../my_deployment_package.zip .;
	cd ..;
	zip -r my_deployment_package.zip *.py;
	rm -rf package;
