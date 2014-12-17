$(function(){

  //Backbone.emulateJSON = false;

  $('#gallery').dropzone({url: 'upload'});

  var PhotoGallery = {};

  PhotoGallery.Album = Backbone.Model.extend({
    url: function(){
      return this.id ? '/albums/' + this.id  : '/albums/'
    },
    defaults: {
      name: 'New Album'
    }
  });

  PhotoGallery.AlbumAddView = Backbone.View.extend({
    el: '#dock .popover',

    initialize: function(){
      $('#new-album').popover('show');
      $('#album-name').val(this.model.get('name'))
      $('#album-name').focus();
    },

    events: {
      'keyup #album-name': 'submitAlbum'
    },

    submitAlbum: function(e){
      if (e.keyCode == 13) {
        this.model.set('name', $(e.currentTarget).val());
        this.model.save({success:function(r){
          $('#new-album').popover('hide');
          console.log(r);
        }});
      };
    }

  });

  PhotoGallery.DockView = Backbone.View.extend({

    el: '#dock',

    events: {
      'click #new-album': 'addAlbum',
    },

    initialize: function(){
      $('#new-album').popover({
        title: 'New Album',
        html: true,
        content: '<input type="text" id="album-name"/>'
      });
    },

    addAlbum: function(e){
      album = new PhotoGallery.Album({})
      new PhotoGallery.AlbumAddView({model: album});
    },

  });

  new PhotoGallery.DockView();

});
