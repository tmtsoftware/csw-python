from csw.CommandResponse import OtherIssue, Invalid, CommandResponse


def test_encode_decode():
    issue=OtherIssue("Bla Bla")
    invalid=Invalid("runId", issue)
    d = invalid._asDict()
    assert Invalid._fromDict(d) == invalid
    assert CommandResponse._fromDict(d) == invalid
