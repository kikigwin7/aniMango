import bleach

tags = [u'li', u'ol', u'ul', u'blockquote', u'sup', u'sub', u'span', u'em', u'strong', u'p', u'h1', u'h2', u'h3', u'h4', u'h5', u'h6', u'a', u'br']
attributes = {
	'*': [u'style'],
	u'a': [u'href'],
}
styles = ['color', 'background-color', 'text-align', 'padding-left', 'text-decoration']
protocols = ['http', 'https']

def bleach_tinymce(str):
	return bleach.clean(
		str,
		tags = tags,
		attributes = attributes,
		styles = styles,
		protocols = protocols,
	)

def bleach_no_tags(str):
	return bleach.clean(
		str,
		tags = [],
		attributes = [],
		styles = [],
		protocols = [],
	)
