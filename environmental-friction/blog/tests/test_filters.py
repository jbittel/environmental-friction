from blog.templatetags.markup import markup


class TestFilters:
    def test_markup(self):
        markup_input = '_How now,_ **brown cow?**'
        html_output = '<p><em>How now,</em> <strong>brown cow?</strong></p>'
        assert markup(markup_input) == html_output
