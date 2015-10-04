Using beanstalkd made easy
==========================

azuki makes it easy to create tools using
[beanstalkd](http://kr.github.io/beanstalkd/) tubes for asynchronous execution.
From queueing parallelizing quick shell hacks to integrating asynchronous
execution with your django application, azuki lets you do it all.

CLI beanstalk inspection
------------------------

The main utility, `azuki`, makes it easy to inspect and modify beanstalk queues
from the command line.

```
$ azuki tubes [-v]
$ azuki stats
$ azuki stats default
$ azuki stats 123
```

The stats command will give you basic statistics, such as the total amount of
connections, jobs and commands.  If you specify a tube, such as `default`, you
will see the statistics of that tube, and if you specify a job ID, you will see
its details and content.

The tubes command shows a list of tubes. Add the -v parameter to also get a
summary of all processes and jobs for all queues.

Peeking at tubes
----------------

```
$ azuki peek-delayed default
$ azuki peek-ready default
$ azuki peek-buried default
$ azuki peek 123
```

With the first three commands above you can look at the first delayed, ready or
buried job in a tube. If you use the `--ask` option as well, you will be asked
whether you want to delete, bury or kick the job. The author is fond of `azuki
peek-buried --ask` to do cleanup of failed jobs.

The last command will peek at a specific job, given its id number.

Manipulating jobs and tubes
---------------------------

`azuki kick 100 default`

This would kick 100 jobs in the default queue, moving them from buried back to
ready.

```
azuki bury 123
azuki kick 123
```

If you want to bury or kick a specific job, use the commands above.

Queueing shell commands
-----------------------
Azuki was originally written to easily parallelize shell jobs. Of course [gnu
parallel](http://www.gnu.org/software/parallel/) can be used if you just want
parallelization, but I also needed to be able to adjust parallelism, pause
everything and add jobs while the application was running. In short, I needed
to use a queue, and beanstalk is my queue of choice.

The original task was to update the iLO firmware of thousands of HP servers in
an automated, yet controlled way. To do this, first one puts jobs in the tube:

```
for ilo in $(<ilos.txt); do
    echo $ilo | azuki put --ttr 600 ilo-firmware
done
```

This reads a list of items and schedules them one by one in the ilo-firmware
tube with a ttr of 600. You can also specify a delay with the `--delay`
argument.

To consume the items in the tube, you use `azuki foreach`.

`azuki foreach ilo-firmware -- xargs do_firmware_update`

The `foreach` command will execute a command you want to execute and feed the
job body on stdin. `do_firmware_update` wants this on the command line instead,
hence the use of `xargs`. To now parallelize this, we can simply run as many
instances of `azuki foreach` as we want in parallel, possibly using screen.

The `foreach` command looks at the exitcode of the commands it runs. If the
exitcode is 0, the job is considered succesfull and gets deleted. If the
exitcode is nonzero, the job gets buried.

At the end of my working day I wanted to pause the upgrading, but using
`ctrl-C` in the middle of a firmware upgrade is not a very good idea. Azuki to
the rescue!

`azuki pause 8640000 ilo-firmware`

This pauses the tube for 100 days. Already running firmware updates would
complete, but no new ones would be scheduled. 10 minutes later all is paused.
To unpause the tube, simply pause it again, but for 0 seconds.

Python API
----------
beanstalkd tubes already are fairly easy to use in python, using the beanstalkc
library. But fairly easy isn't easy enough, so azuki can make it easier for
you. You can simply decorate your functions to make them asynchronous.

example.py:
```
from azuki import beanstalk

@beanstalk('example-tube')
def hello(who):
    print "Hello, %s" % who
```

main.py:
```
import example

example.hello("world")
```

If you now run `python main.py`, you will notice that it does not output
anything. Instead it has serialized the arguments to `hello` and scheduled them
as a job in the `example-tube` tube.

To process the queued jobs, you run `azuki daemon example-tube`. This will take
items from the tube, import the `example` module and call the `hello` function
for real.

Rescheduling
------------
With beanstalk you can bury a job to tell beanstalk not to attempt the job
again until manually told to do so, but if you just want to delay execution of
a job, you can raise an `azuki.Reschedule` exception.

```
from azuki import beanstalk, Reschedule

@beanstalk('example-tube')
def process(task):
    if not am_ready_for(task):
        raise Reschedule(120)
    do_task(task)
```

Django API
----------
The downside of scheduling things in beanstalk queues, is that argument to
function calls must be serialized. Azuki uses json serialization, so anything
that is not json-serializable, cannot be used as an argument.

Except django model instances, as azuki recognizes them and handles them
specially. That means that for example queueing mails instead of sending them
directly works:

models.py:
```
from django.contrib.auth import User
from django.core.mail import send_mail
from azuki import beanstalk

class Message(models.Model):
    recipient = models.ForeignKey(User)
    subject = models.CharField("Subject", max_length=128)
    text = models.TextField("Message text")

    @beanstalk('send-mail')
    def send(self):
        send_mail(self.subject, self.text, 'webmaster@localhost', [self.recipient])
```

If you now create a message and call `send()`, the message is not sent, but
only added to the `send-mail` tube. You can again use `azuki daemon` to process
this tube and actually send the mails, possibly even on a different machine
altogether.

Author
------
(c) 2014, Dennis Kaarsemaker <dennis@kaarsemaker.net>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
