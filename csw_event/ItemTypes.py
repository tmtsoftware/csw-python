from csw_protobuf.parameter_types_pb2 import IntItems


class IntArray:

    def __init__(self, values):
        ar = []
        for i in values:
            item = IntItems()
            item.values.extend(i)
            ar.append(item)
        self.items = ar

