#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/noa/catkin_ws/src/move_turtle"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/noa/catkin_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/noa/catkin_ws/install/lib/python2.7/dist-packages:/home/noa/catkin_ws/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/noa/catkin_ws/build" \
    "/usr/bin/python" \
    "/home/noa/catkin_ws/src/move_turtle/setup.py" \
    build --build-base "/home/noa/catkin_ws/build/move_turtle" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/noa/catkin_ws/install" --install-scripts="/home/noa/catkin_ws/install/bin"
