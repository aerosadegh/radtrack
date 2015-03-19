#### Running radtrack in a docker container

Get DISPLAY variable:

```bash
echo $DISPLAY
```

Get xauth for that display

```bash
xauth list
```

Set up a tunnel on the host (6000 + display):

```
socat TCP-LISTEN:6010,fork,bind=172.17.42.1 TCP:127.0.0.1:6010
```

Note: the 172.17.42.1 will change, but this is the docker default for the docker host.

Add in the xauth cookie from above:

```
xauth add 172.17.42.1:10 MIT-MAGIC-COOKIE-1  <cookie>
```

In docker container, set the display:

```
export DISPLAY=172.17.42.1:10.0
```

Start the display.
