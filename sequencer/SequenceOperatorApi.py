from esw.EswSequencerResponse import PullNextResponse, MaybeNextResult, Unhandled
from esw.Step import Step
from sequencer.SequencerApi import SequencerApi


class SequenceOperatorHttp:
    """
    This trait is to help execution of stepList(Sequence)
    """

    def __init__(self, seq: SequencerApi):
        self.seq = seq

    def pullNext(self) -> PullNextResponse:
        """
        This method sends a PullNext message to sequencer if successful it returns the pending step which is to be executed next
        """
        return self.seq.pullNext()

    def maybeNext(self) -> Step | None:
        """
        This method returns the next step Pending step if sequencer is in Running state otherwise returns None
        """
        x = self.seq.maybeNext()
        match x:
            case MaybeNextResult():
                r: MaybeNextResult = x
                return r.maybeStep
            case Unhandled():
                return None

# /**
#  * This method is to determine whether next step is ready to execute or not. It returns Ok if the next step is ready for execution
#  * otherwise it waits until it is ready to execute and then returns the Ok response.
#  * Unhandled is returned when the ReadyToExecuteNext message is not acceptable by sequencer
#  *
#  * @return a [[esw.ocs.api.protocol.OkOrUnhandledResponse]] as Future value
#  */
# def readyToExecuteNext: Future[OkOrUnhandledResponse] = seqF.flatMap(_.get.readyToExecuteNext)
#
# /**
#  * This method changes the status from InFlight to [[esw.ocs.api.models.StepStatus.Finished.Success]](Finished) for current running step
#  */
# def stepSuccess(): Unit =
#   seqF.flatMap(x => Future.successful(x.get.stepSuccess()))
#
# /**
#  * This method changes the status from InFlight to [[esw.ocs.api.models.StepStatus.Finished.Failure]](Finished) for current running step
#  */
# def stepFailure(message: String): Unit =
#   seqF.flatMap(x => Future.successful(x.get.stepFailure(message)))
