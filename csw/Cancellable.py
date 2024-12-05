class Cancellable:
    """
    API for a scheduled periodic task, that allows it to be cancelled.
    """
    def cancel(self) -> bool:
        """
        Cancels this Cancellable and returns true if that was successful.
        If this cancellable was (concurrently) cancelled already, then this method
        will return false.

        Returns:
            whether or not the cancellable was cancelled successfully
        """
        pass
