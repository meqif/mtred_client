# mtred_client

A simple client for the [Mt. Red Mining Pool](https://www.mtred.com).

## Usage

`python mtred.py [API key]`

## Tips and Tricks

If you're running OSX and have [Growl](http://growl.info/) installed, you can use [`growlnotify`](http://growl.info/extras.php) to get regular notifications, like this:

![](https://github.com/meqif/mtred_client/raw/master/growl_notification.png)

    while true; do
        (echo "Mt.Red Pool" ; python mtred.py yourapikeyhere) | growlnotify --image ~/Downloads/bitcoin.png;
        sleep 60
    done
