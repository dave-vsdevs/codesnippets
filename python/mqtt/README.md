*What is it?*

This is a very basic implementation of a SEND ONLY mqtt client.

*Why??*

I have a number of scripts running all over the place.   I have been looking for a way to
get these scripts to be able to report errors/info back to a central location that then could
notify me of any issues via a daily digest email or a urgent email.

Issues here are I have a existing logging library but I try to keep it as simple as possible
to reduce any dependance needs and any possiblity of it triggering exceptions.

So this is about as basic as you can get - no need for Paho just struct and socket.

Plus the whole thing is wrapped to prevent it causing a exception.   From my point of view at least
for these personal types of script you don't want your debugging/reporting system to cause errors

The point is to catch errors.

So this just returns True if it was able to send and returns false if there was a error (and prints to stderr)

do_connect(client_id="TestMTQQ",server="127.0.0.1", port=1883,topic="Topic1",message='XX'.zfill(2097000))

It should also support SSL and authentication - these work for me using mosquitto and a self signed cert

----But they didn't work when I tried to use a cloud based MQTT server so maybe there is a issue there....

I have had a lot of good results decoupling scripts from each other using MQTT this is just another step along that path



