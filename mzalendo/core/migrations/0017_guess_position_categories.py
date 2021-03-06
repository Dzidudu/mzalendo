# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


def set_category(category, qs):
    """set the category for all 'other' items in the qs"""
    for obj in qs.filter(category='other'):
        obj.category = category
        obj.save()



class Migration(DataMigration):
    
    def forwards(self, orm):
        "Try to guess which category based on various constraints"
    
        positions = orm.Position.objects.all()
    
        # all the following slugs are political
        for slug in [ 'mp' ]:
            set_category(
                'political',
                positions.filter(title__slug=slug)
            )

        # Anything to do with a political party is political
        set_category(
            'political',
            positions.filter(organisation__kind__slug='party')
        )
    
        # If it starts with minister it probably is
        set_category(
            'political',
            positions.filter(title__name__startswith='Minister')
        )
        
        # Anything for parliament is political
        for slug in ['parliament','parliament-of-the-republic-of-kenya']:
            set_category(
                'political',
                positions.filter(organisation__slug=slug)
            )
    
        # Catch the students
        for name in ['Student', 'Undergraduate Student']:
            set_category(
                'education',
                positions.filter(title__name=name)
            )
    
    def backwards(self, orm):
        "Set all category choices back to the default 'other'"
        for pos in orm.Position.objects.all():
            pos.category = 'other'
            pos.save()
    

    models = {
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.contact': {
            'Meta': {'object_name': 'Contact'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74187)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ContactKind']"}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'source': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74264)', 'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'core.contactkind': {
            'Meta': {'object_name': 'ContactKind'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74187)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74264)', 'auto_now': 'True', 'blank': 'True'})
        },
        'core.informationsource': {
            'Meta': {'object_name': 'InformationSource'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74187)', 'auto_now_add': 'True', 'blank': 'True'}),
            'entered': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74264)', 'auto_now': 'True', 'blank': 'True'})
        },
        'core.organisation': {
            'Meta': {'object_name': 'Organisation'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74187)', 'auto_now_add': 'True', 'blank': 'True'}),
            'ended': ('django_date_extensions.fields.ApproximateDateField', [], {'max_length': '10', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.OrganisationKind']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'original_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'started': ('django_date_extensions.fields.ApproximateDateField', [], {'max_length': '10', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74264)', 'auto_now': 'True', 'blank': 'True'})
        },
        'core.organisationkind': {
            'Meta': {'object_name': 'OrganisationKind'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74187)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74264)', 'auto_now': 'True', 'blank': 'True'})
        },
        'core.person': {
            'Meta': {'object_name': 'Person'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74187)', 'auto_now_add': 'True', 'blank': 'True'}),
            'date_of_birth': ('django_date_extensions.fields.ApproximateDateField', [], {'max_length': '10', 'blank': 'True'}),
            'date_of_death': ('django_date_extensions.fields.ApproximateDateField', [], {'max_length': '10', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legal_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'original_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'other_names': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74264)', 'auto_now': 'True', 'blank': 'True'})
        },
        'core.place': {
            'Meta': {'object_name': 'Place'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74187)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.PlaceKind']"}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Organisation']", 'null': 'True', 'blank': 'True'}),
            'original_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'shape_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74264)', 'auto_now': 'True', 'blank': 'True'})
        },
        'core.placekind': {
            'Meta': {'object_name': 'PlaceKind'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74187)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74264)', 'auto_now': 'True', 'blank': 'True'})
        },
        'core.position': {
            'Meta': {'object_name': 'Position'},
            'category': ('django.db.models.fields.CharField', [], {'default': "'other'", 'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74187)', 'auto_now_add': 'True', 'blank': 'True'}),
            'end_date': ('django_date_extensions.fields.ApproximateDateField', [], {'default': "'future'", 'max_length': '10', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'blank': 'True'}),
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Organisation']", 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Person']"}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Place']", 'null': 'True', 'blank': 'True'}),
            'start_date': ('django_date_extensions.fields.ApproximateDateField', [], {'max_length': '10', 'blank': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.PositionTitle']", 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74264)', 'auto_now': 'True', 'blank': 'True'})
        },
        'core.positiontitle': {
            'Meta': {'object_name': 'PositionTitle'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74187)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'original_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 25, 14, 48, 21, 74264)', 'auto_now': 'True', 'blank': 'True'})
        },
        'images.image': {
            'Meta': {'object_name': 'Image'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        }
    }
    
    complete_apps = ['core']
