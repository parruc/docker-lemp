FROM php:fpm
RUN docker-php-ext-install mysqli
#RUN apt-get update && apt-get install -y libfreetype6-dev libjpeg62-turbo-dev libmcrypt-dev libpng12-dev && rm -rf /var/lib/apt/lists/*
#RUN docker-php-ext-install iconv 
#RUN docker-php-ext-install mcrypt
#RUN docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/
#RUN docker-php-ext-install gd
