from eduserver.db_controller import DBController


class Controller:
    def get_results_by_filter(self, filter):
        db_controller = DBController()
        # return db_controller.get_results_by_user()
        # if (filter.min is None and filter.max is None and filter.start is None and filter.end is None):
        #     print("here")

        self.validate_filter(filter)
        results = db_controller.get_results_by_user()
        results = self.filter_by_date(results, filter.start, filter.end)
        results = self.filter_by_results(results, filter.min, filter.max)
        return results

    def validate_filter(self, filter):
        if (filter.min is None or filter.max is None):
            raise Exception("Min and max can't be empty!")
        if (filter.start is None or filter.end is None):
            raise Exception("Start and end date can't be empty!")
        if (filter.start > filter.end):
            raise Exception("Start can't be later than end!")

    def filter_by_date(self, arr, start, end):
        results = []
        for item in arr:
            if (item.date >= start and item.date <= end):
                results.append(item)
        return results

    def filter_by_results(self, arr, min, max):
        if (min > max):
            min, max = max, min
        results = []
        for item in arr:
            if (item.result >= min and item.result <= max):
                results.append(item)
        return results