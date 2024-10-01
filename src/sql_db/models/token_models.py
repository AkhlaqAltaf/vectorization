from src.views import db

# Association table (through-table) for MetaData and Token

class ParagraphMetaData(db.Model):
    __tablename__ = 'paragraph_metadata'
    id = db.Column(db.Integer, primary_key=True)
    paragraph_id = db.Column(db.Integer, db.ForeignKey('paragraphs.id'), nullable=False,unique=False)
    metadata_id = db.Column(db.Integer, db.ForeignKey('metadata.id'), nullable=False,unique=False)
    char_start_pos = db.Column(db.Integer, nullable=True)

    # Ensure a combination of token_id and metadata_id is unique
    __table_args__ = (db.UniqueConstraint('paragraph_id', 'metadata_id',"char_start_pos", name='_paragraph_metadata_uc'),)

    def __repr__(self):
        return f'<ParagraphMetaData Paragraph ID: {self.paragraph_id}, MetaData ID: {self.metadata_id}>'


# Token model
class Paragraph(db.Model):
    __tablename__ = 'paragraphs'
    id = db.Column(db.Integer, primary_key=True)
    paragraph_value = db.Column(db.Text, nullable=False)  # Ensure token is unique globally
    metadata_associations = db.relationship('ParagraphMetaData', backref='paragraph', lazy=True)



# SENTENCE LEVEL DATA

class SentenceMetaData(db.Model):
    __tablename__ = 'sentence_metadata'
    id = db.Column(db.Integer, primary_key=True)
    sentence_id = db.Column(db.Integer, db.ForeignKey('sentences.id'), nullable=False,unique=False)
    metadata_id = db.Column(db.Integer, db.ForeignKey('metadata.id'), nullable=False,unique=False)
    char_start_pos = db.Column(db.Integer, nullable=True)

    # Ensure a combination of token_id and metadata_id is unique
    __table_args__ = (db.UniqueConstraint('sentence_id', 'metadata_id',"char_start_pos",  name='_sentence_metadata_uc'),)

    def __repr__(self):
        return f'<SentenceMetaData Sentence ID: {self.token_id}, MetaData ID: {self.metadata_id}>'


# Token model
class Sentence(db.Model):
    __tablename__ = 'sentences'
    id = db.Column(db.Integer, primary_key=True)
    sentence_value = db.Column(db.String(255), nullable=False)  # Ensure token is unique globally
    metadata_associations = db.relationship('SentenceMetaData', backref='sentence', lazy=True)


# WORD LEVEL DATA
class WordMetaData(db.Model):
    __tablename__ = 'word_metadata'
    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), nullable=False,unique=False)
    metadata_id = db.Column(db.Integer, db.ForeignKey('metadata.id'), nullable=False,unique=False)
    char_start_pos = db.Column(db.Integer, nullable=True)

    # Ensure a combination of token_id and metadata_id is unique
    __table_args__ = (db.UniqueConstraint('word_id', 'metadata_id', "char_start_pos", name='_word_metadata_uc'),)

    def __repr__(self):
        return f'<WordMetaData Word ID: {self.word_id}, MetaData ID: {self.metadata_id}>'


# Token model
class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    word_value = db.Column(db.String(255), nullable=False, unique=True)  # Ensure token is unique globally
    metadata_associations = db.relationship('WordMetaData', backref='word', lazy=True)


# PHRASE LEVEL DATA
class PhraseMetaData(db.Model):
    __tablename__ = 'phrase_metadata'
    id = db.Column(db.Integer, primary_key=True)
    phrase_id = db.Column(db.Integer, db.ForeignKey('phrases.id'), nullable=False,unique=False)
    metadata_id = db.Column(db.Integer, db.ForeignKey('metadata.id'), nullable=False,unique=False)
    char_start_pos = db.Column(db.Integer, nullable=True)

    # Ensure a combination of token_id and metadata_id is unique
    __table_args__ = (db.UniqueConstraint('phrase_id', 'metadata_id',"char_start_pos", name='_phrase_metadata_uc'),)

    def __repr__(self):
        return f'<PhraseMetaData Phrase ID: {self.phrase_id}, MetaData ID: {self.metadata_id}>'


# Token model
class Phrase(db.Model):
    __tablename__ = 'phrases'
    id = db.Column(db.Integer, primary_key=True)
    phrase_value = db.Column(db.String(255), nullable=False, unique=True)  # Ensure token is unique globally
    metadata_associations = db.relationship('PhraseMetaData', backref='phrase', lazy=True)

class TokenMetaData(db.Model):
    __tablename__ = 'token_metadata'
    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.Integer, db.ForeignKey('tokens.id'), nullable=False,unique=False)
    metadata_id = db.Column(db.Integer, db.ForeignKey('metadata.id'), nullable=False,unique=False)
    char_start_pos = db.Column(db.Integer, nullable=True)

    # Ensure a combination of token_id and metadata_id is unique
    __table_args__ = (db.UniqueConstraint('token_id', 'metadata_id',"char_start_pos",  name='_token_metadata_uc'),)

    def __repr__(self):
        return f'<TokenMetaData Token ID: {self.token_id}, MetaData ID: {self.metadata_id}>'


# Token model
class Token(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    token_value = db.Column(db.String(255), nullable=False, unique=True)  # Ensure token is unique globally
    metadata_associations = db.relationship('TokenMetaData', backref='token', lazy=True)

    def __repr__(self):
        return f'<Token {self.token_value}>'


# MetaData model
class MetaData(db.Model):
    __tablename__ = 'metadata'
    id = db.Column(db.Integer, primary_key=True)
    paragraph_number = db.Column(db.Integer, nullable=True)
    full_text = db.Column(db.Text, nullable=True)
    topic = db.Column(db.Text, nullable=True)
    text_preview = db.Column(db.Text, nullable=True)
    question = db.Column(db.Text, nullable=True)
    link = db.Column(db.Text, nullable=True)
    page_id = db.Column(db.Integer, nullable=True)
    row_number = db.Column(db.Integer, nullable=True)
    token_count = db.Column(db.Integer, nullable=True)

    # Many-to-many relationship via the association table
    tokens = db.relationship('TokenMetaData', backref='metadata', lazy=True)

    entities = db.relationship('Entity', backref='metadata', lazy=True)

    def __repr__(self):
        return f'<MetaData ID: {self.id}, Paragraph: {self.paragraph_number}>'


# Entity model (unchanged)
class Entity(db.Model):
    __tablename__ = 'entities'
    id = db.Column(db.Integer, primary_key=True)
    entity_value = db.Column(db.String(255), nullable=False)
    entity_type = db.Column(db.String(50), nullable=False)  # Entity type (e.g., ORG, PERSON, etc.)
    metadata_id = db.Column(db.Integer, db.ForeignKey('metadata.id'), nullable=False)

    def __repr__(self):
        return f'<Entity {self.entity_value} ({self.entity_type})>'
