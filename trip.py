import datetime


class Trip:

    def __init__(self):
        self.Origin = "ORY"
        self.Destination = "AMS"
        self.OutboundDate = datetime.datetime(2019, 10, 10)
        self.InboundDate = datetime.datetime(2019, 10, 17)

    def data(self):
        return {"routeSelection.DepartureStation": self.Origin,
                "routeSelection.ArrivalStation": self.Destination,
                "dateSelection.OutboundDate.Day": self.OutboundDate.day,
                "dateSelection.OutboundDate.Month": self.OutboundDate.month,
                "dateSelection.OutboundDate.Year": self.OutboundDate.year,
                "dateSelection.IsReturnFlight": "true",
                "dateSelection.InboundDate.Day": self.InboundDate.day,
                "dateSelection.InboundDate.Month": self.InboundDate.month,
                "dateSelection.InboundDate.Year": self.InboundDate.year,
                "selectPassengersCount.AdultCount": "1",
                "selectPassengersCount.ChildCount": "0",
                "selectPassengersCount.InfantCount": "0",
                "flyingBlueSearch.FlyingBlueSearch": "false"}
