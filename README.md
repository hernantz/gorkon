======
GORKON
======
![Gorkon](http://fc09.deviantart.net/fs4/i/2004/221/b/7/Orc_Shaman.jpg)


Tiny webapp built on top of redis, celery, youtube-dl and flask that, provided
a youtube|vimeo|soundcloud|blip.tv link, will download the media file and
optionally convert the output to other format.


TODO
====
* TESTS!!!1.
* Automated deployment.
* Use FlexBox for fun.
* Allow to queue multiple simultaneous downloads.
* Use celery [chains][chains]. Did not work when [tried][stackoverflow].


[chains]: https://github.com/requirejs/text "Celery chains documentation"
[stackoverflow]: http://stackoverflow.com/questions/16306175/get-progress-from-async-python-celery-chain-by-chain-id "Get progress from async python celery chain by chain id"
