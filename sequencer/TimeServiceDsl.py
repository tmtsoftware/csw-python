# /**
#  * Kotlin Dsl for scheduling periodic/non-periodic tasks at a specified time and/or interval.
#  * This Dsl provides simplified APIs over csw time service dsl, and some utility methods for scripts.
#  * It supports scheduling on both [[csw.time.core.models.UTCTime]] and [[csw.time.core.models.TAITime]].
#  * Each API returns a [[Cancellable]] which allows users to cancel the execution of tasks.
#  */
# interface TimeServiceDsl : SuspendToJavaConverter {
#     val timeService: TimeServiceScheduler
#
#     /**
#      * Schedules task once at specified time. Callbacks like task are thread safe as they are executed on single threaded coroutine scope dispatcher.
#      *
#      * @param startTime the time at which the task should start its execution
#      * @param task the task to be scheduled for execution
#      * @return a handle to cancel the execution of the task if it hasn't been executed already
#      */
#     fun scheduleOnce(startTime: TMTTime, task: SuspendableCallback): Cancellable =
#             timeService.scheduleOnce(startTime, Runnable { task.toJava() })
#
#     /**
#      * Schedules task once at duration after current utc time. Callbacks like task are thread safe as they are executed on single threaded coroutine scope dispatcher.
#      *
#      * @param delayFromNow delay after which task will be scheduled as a Duration
#      * @param task the task to be scheduled for execution
#      * @return a handle to cancel the execution of the task if it hasn't been executed already
#      */
#     fun scheduleOnceFromNow(delayFromNow: Duration, task: SuspendableCallback): Cancellable =
#             scheduleOnce(utcTimeAfter(delayFromNow), task)
#
#     /**
#      * Schedules a task to execute periodically at the given interval. The task is executed once at the given start time followed by execution of task at each interval.
#      * Callbacks like task are thread safe as they are executed on single threaded coroutine scope dispatcher.
#      *
#      * @param startTime first time at which task is to be executed
#      * @param interval the time interval between the execution of tasks
#      * @param task the task to execute after each interval
#      * @return a handle to cancel the execution of further tasks
#      */
#     fun schedulePeriodically(startTime: TMTTime, interval: Duration, task: SuspendableCallback): Cancellable =
#             timeService.schedulePeriodically(
#                     startTime,
#                     interval.toJavaDuration(),
#                     Runnable { task.toJava() })
#
#     /**
#      * Schedules a task to execute periodically at the given interval. The task is executed immediately and then after every provided duration.
#      * Callbacks like task are thread safe as they are executed on single threaded coroutine scope dispatcher.
#      *
#      * @param interval the time interval between the execution of tasks
#      * @param task the task to execute after each interval
#      * @return a handle to cancel the execution of further tasks
#      */
#     fun schedulePeriodically(interval: Duration, task: SuspendableCallback): Cancellable =
#             timeService.schedulePeriodically(
#                     interval.toJavaDuration(),
#                     Runnable { task.toJava() })
#
#     /**
#      * Schedules a task to execute periodically at the given interval. The task is executed once at duration after current utc time
#      * followed by execution of task at each interval. Callbacks like task are thread safe as they are executed on single threaded coroutine scope dispatcher.
#      *
#      * @param delayFromNow delay after which the first task will be scheduled as a Duration
#      * @param interval the time interval between the execution of tasks
#      * @param task the task to execute after each interval
#      * @return a handle to cancel the execution of further tasks
#      */
#     fun schedulePeriodicallyFromNow(
#             delayFromNow: Duration,
#             interval: Duration,
#             task: SuspendableCallback
#     ): Cancellable =
#             schedulePeriodically(utcTimeAfter(delayFromNow), interval, task)
#
#     /**
#      * Utility to calculate current utc time
#      *
#      * @return current utc time
#      */
#     fun utcTimeNow(): UTCTime = UTCTime.now()
#
#     /**
#      * Utility to calculate current tai time
#      *
#      * @return current tai time
#      */
#     fun taiTimeNow(): TAITime = TAITime.now()
#
#     /**
#      * Utility to calculate utc time after specified duration
#      *
#      * @param duration time duration
#      * @return utc time after specified time duration
#      *
#      */
#     fun utcTimeAfter(duration: Duration): UTCTime =
#             UTCTime.after(FiniteDuration(duration.inWholeNanoseconds, TimeUnit.NANOSECONDS))
#
#     /**
#      * Utility to calculate tai time after specified duration
#      *
#      * @param duration time duration
#      * @return tai time after specified time duration
#      *
#      */
#     fun taiTimeAfter(duration: Duration): TAITime =
#             TAITime.after(FiniteDuration(duration.inWholeNanoseconds, TimeUnit.NANOSECONDS))
#
#     /**
#      * Extension method on TMT time to calculate offset from it
#      *
#      * @return offset from utc/tai time
#      */
#     fun TMTTime.offsetFromNow(): Duration = durationFromNow().toNanos().nanoseconds
#
# }
