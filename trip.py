import datetime


class Trip:

    def __init__(self):
        self.token = None
        self.Origin = "ORY"
        self.Destination = "AMS"
        self.OutboundDate = datetime.datetime(2019, 10, 10)
        self.InboundDate = datetime.datetime(2019, 10, 17)
        self.hasFetchedStep1 = False
        self.hasResponseStep1 = False
        self.hasFetchedStep2 = False
        self.hasFetchedStep3 = False

    def settoken(self, token):
        self.token = token

    def setstep1(self):
        self.hasFetchedStep1 = True

    def setstep2(self):
        self.hasFetchedStep2 = True

    def sethasresponsestep1(self):
        self.hasResponseStep1 = True

    def data(self):
        return {"__RequestVerificationToken": self.token,
                "routeSelection.DepartureStation": self.Origin,
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

    def availdataoutbound(self):
        return {"selectSingleDayAvailability.JourneyType": 'SingleDayOutbound',
                "selectSingleDayAvailability.Date.DateToParse": self.OutboundDate.strftime('%Y-%m-%d'),
                "selectSingleDayAvailability.AutoSelect": "true",
                "__RequestVerificationToken": self.token, }

    def availdatainbound(self):
        return {"selectSingleDayAvailability.JourneyType": 'SingleDayInbound',
                "selectSingleDayAvailability.Date.DateToParse": self.InboundDate.strftime('%Y-%m-%d'),
                "selectSingleDayAvailability.AutoSelect": "true",
                "__RequestVerificationToken": self.token, }
