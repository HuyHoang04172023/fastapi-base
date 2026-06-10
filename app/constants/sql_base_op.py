from constants.base import BaseEnum


class SqlBasicOp(str, BaseEnum):
    EQ = 'eq', "Equal (==)"
    NE = 'ne', "Not equal (!=)"
    GT = 'gt', "Greater than (>)"
    LT = 'lt', "Lower than (<)"
    GE = 'ge', "Greater equal (>=)"
    LE = 'le', "Lower equal (<=)"
    LIKE = 'like', "Like (need add %)"
    ILIKE = 'ilike', "iLike (need add %)"
    IN = 'in', "IN"
    IS = 'is', "IS"
