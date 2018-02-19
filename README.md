# Boxrec
This repository provides a very simple Python wrapper around the Boxrec.com website. The goal is to provide an easy way to access the information presented on the Boxrec website without having to go through the whole DOM-tree yourself.

# How do I use this?
The easiest way to instantiate a full representation of fights and boxers on boxrec.com is to use the `FightServiceFactory.make_service()` method in `boxrec.services`. An example is given below
```{python}
from boxrec.services import FightServiceFactory
fight_service = FightServiceFactory.make_service()

result = fight_service.find_by_id({event_id}, {fight_id})
```
The variable result now contains statistics of the fight, and also contains references to objects representing the two boxers involved.

# Why is this repository so nicely structured / extremely verbose (take your pick!)
My goal is to also use this repository for the testing course in the masterclass. Therefore, it is structured in a way that will facilitate myself explaining about dependency injection/factory patterns etc. The consequence of this is that the code is slightly verbose...

# Some words on authentication
I've noticed that after a certain amount of requests Boxrec seems to require authentication for you to view any extra pages. Currently, this library does no facilitate this. However you can pass a `requests` Session object to the `FightServiceFactory.make_service()` method. Your service will then use this session for any communication to the Boxrec website. You should be able to authenticate in this session yourself.