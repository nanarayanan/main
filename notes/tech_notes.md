Tech Notes

# Even-Driven Architecture

## References

1. [The Many Meanings of Event-Driven Architecture • Martin Fowler • GOTO
   2017](https://www.youtube.com/watch?v=STKCRSUsyP0&t=520s) [What do you mean
   by
   “Event-Driven”?](https://martinfowler.com/articles/201701-event-driven.html)

   1. Presence of one of more of the following four patterns:
	  1. **Event Notification by reversing dependencies**: Consider a scenario
	     where a customer address change requires a change in insurance quote,
	     hence Customer Mgmt subsystem needs to invoke the Insurance Quote
	     subsystem. However, having such a dependency between a generic
	     subsystem like Customer Management on Insurance Quote subsystem doesn't
	     make sense and we need to reverse the dependency. One way to achieve
	     this is to make Customer Mgmt send a notification as and when there is
	     a change in a customer's address and the interested subsystems can
	     query Customer Mgmt to identify what changed. This can result in too
	     many subsystems sending a query to Customer Mgmt on an address change
	     and we can make the event notification to include additional data:
	     customer name, old address and the new address.
	  2. **Event-carried State Transfer**: Going by the above scenario, Customer
	     Mgmt subsystem can broadcast data about a customer as and when there is
	     some change and the interested subsystems can look at the notification
	     data and cache the portion of the data relevant to them locally. This
	     results in avoidance of queries to Customer Mgmt, however this has the
	     problem of some subsystem's local cache not being in sync always,
	     though it can become eventually consistent. The advantages of (a)
	     Decoupling between the subsystems, (b) Reduced load on supplier, (c)
	     Replicated Data need to be weighed against the impact due to local
	     cached data not always being consistent.
	  3. **Event Sourcing**: Every events as it occurs is first persisted in a
	     Log and then acted upon to effect a change in the Application State. If
	     done the right way, it should be possible to recreate the Application
	     State anytime by just replaying the events in the Log. One of the best
	     examples of Event Sourcing system is **Version Control**. Note that we
	     don't need to hold onto all the Events in the Log forever and instead
	     we can have Snapshots taken periodically that reflect the interim views
	     of the Application State. Event Sourcing can be looked at as a way of
	     providing your end-users a system that works on their data similar to
	     how a Version Control system works on your source code. Accounting
	     Ledgers maintained in the financial world is another good example. One
	     of the items to be looked at is how to capture both the Events --- one
	     associated with the intention behind change (business logic) and the
	     other relating to the actual change. Considering Version Control as an
	     example, the developer may intend to change a variable name for better
	     readability and this results in lot of textual changes in the code. How
	     does one capture both these Events?
	  4. **CQRS: Command Query Responsibility Segration** Different models for
	     reading and updates. This can be complex.

# Microservices

## References

1. [Creating event-driven microservices: the why, how and what by Andrew
   Schofield](https://www.youtube.com/watch?v=ksRCq0BJef8)

   1. What are microservices?

      Microservices is a technique for structuring an app as a collection of
      services.
	  * Self-contained with clear interfaces and a distinct purpose.
	  * Loosely coupled --- communicate over the network.
	  * Independently deployable, scalable, maintainable and testable.

   2. Patterns for event-driven microservices?

      You want:
	  * Loose coupling
	  * Data consistency
	  * Efficient queries

	  You need **Patterns** such as:
	  * Database per Service
	  * Saga
	  * Event sourcing
	  * CQRS (Command Query Responsibility Segregation)
