test aws

aws s3api create-bucket --bucket fidworkstatic --region gra --acl public-read --endpoint-url https://s3.gra.io.cloud.ovh.net
aws s3 cp index.html s3://fidworkstatic/index.html   --endpoint-url https://s3.gra.io.cloud.ovh.net --acl public-read --content-type text/html
aws s3 cp error.html s3://fidworkstatic/error.html   --endpoint-url https://s3.gra.io.cloud.ovh.net --acl public-read --content-type text/html


aws s3 website s3://fidworkstatic  --index-document index.html --error-document error.html --endpoint-url https://s3.gra.io.cloud.ovh.net/

on obtient : 
http://fidworkpublic.s3-website.gra.io.cloud.ovh.net/