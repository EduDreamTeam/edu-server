#/usr/bin/bash

export JWT_AUTH_PREFIX=JWT
export JWT_AUTH_TOKEN=super-secret

http POST localhost:5000/register firstName=simon lastName=pav email=mail@ex.com login=simon__p password=1234

http localhost:5000/auth login=wrong_login password=1234
http localhost:5000/auth login=simon__p password=wrong_pwd

token=`http localhost:5000/auth login=simon__p password=1234 | grep token | sed 's/"//g' | awk '{print $2}'`
echo TOKEN: $token

http --auth-type jwt -a $token localhost:5000/userinfo

