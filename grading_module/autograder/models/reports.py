class TestSuiteReport:
    def __init__(self, question, source_file, report_files, points_available, points_earned, messages=[]):
        self.question = question
        self.source_file = source_file
        self.points_available = points_available
        self.points_earned = points_earned
        self.messages = messages
        self.report_files = report_files

    def __str__(self):
        return f'Q: {self.question}, file {self.source_file}, reports {self.report_files}, pts {self.points_available}, earned {self.points_earned}, messages {self.messages}'


    def JSONRepr(self):
        return {
            "question": self.question,
            "source_file": self.source_file,
            "points_available": self.points_available,
            "points_earned": self.points_earned,
            "messages": self.messages,
            "report_files": self.report_files
        }
