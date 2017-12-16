#/usr/bin/bash

export JWT_AUTH_PREFIX=JWT
export JWT_AUTH_TOKEN=super-secret

http POST localhost:5000/register firstName=simon lastName=pav email=mail@ex.com login=simon__p password=1234

http localhost:5000/auth login=wrong_login password=1234
http localhost:5000/auth login=simon__p password=wrong_pwd

token=`http localhost:5000/auth login=simon__p password=1234 | grep token | sed 's/"//g' | awk '{print $2}'`
echo TOKEN: $token

http --auth-type jwt -a $token localhost:5000/userinfo

http --auth-type jwt -a $token localhost:5000/dict
http --auth-type jwt -a $token GET localhost:5000/dict word=word2
http --auth-type jwt -a $token GET localhost:5000/dict word=error_word

http --auth-type jwt -a $token localhost:5000/dict word=freedom translate:='["свобода"]'
http --auth-type jwt -a $token localhost:5000/dict word=life    translate:='["жизнь"]'
http --auth-type jwt -a $token localhost:5000/dict word=island  translate:='["остров"]'
http --auth-type jwt -a $token localhost:5000/dict word=rage    translate:='["ярость", "гнев"]'
http --auth-type jwt -a $token localhost:5000/dict word=dog     translate:='["собака", "пёс"]'
http --auth-type jwt -a $token localhost:5000/dict word=cat     translate:='["кошка"]'
http --auth-type jwt -a $token localhost:5000/dict word=boll    translate:='["мячь"]'
http --auth-type jwt -a $token localhost:5000/dict word=cat     translate:='["кошка", "кот"]'
http --auth-type jwt -a $token localhost:5000/dict

http --auth-type jwt -a $token localhost:5000/task
http --auth-type jwt -a $token localhost:5000/task
http --auth-type jwt -a $token localhost:5000/task
http --auth-type jwt -a $token localhost:5000/task
http --auth-type jwt -a $token localhost:5000/task

