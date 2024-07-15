#!/bin/sh

gpio_nums=27

for i in $(seq 1 $gpio_nums); do
  gpioset 0 $i=1 || echo "Pin $i does not exist!\n"

  printf "GPIO-$i\n"
done