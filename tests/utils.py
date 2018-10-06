import attr


@attr.s
class User:
	points = attr.ib(type=int)
