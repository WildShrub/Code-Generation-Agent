The following are some best practices when working with code from multiple different files.

## If a function or class from a separate file needs to be accessed, it must be imported at the top of the file
    for example, let's say there are 2 files named event_list.py and event.py. event.py contains the class called Event, in order for the Event class to be used in event_list.py, the Event class must be imported at the top of the file, like this:
    
    from event import Event

    the Event class can then be used as normal



