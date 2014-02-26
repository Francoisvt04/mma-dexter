(function($, exports) {
  if (typeof exports.Dexter == 'undefined') exports.Dexter = {};
  var Dexter = exports.Dexter;

  // view when editing document details (NOT the analysis)
  Dexter.EditDocumentView = function() {
    var self = this;

    self.init = function() {
      if ($('#new-document, #edit-document').length === 0) {
        return;
      }

      // author name autocomplete
      self.$authorWidget = $('.author-widget');
      self.authorHound = new Bloodhound({
        name: 'authors',
        prefetch: {
          url: '/api/authors',
          ttl: 60,
          filter: function(resp) { return resp.authors; },
        },
        datumTokenizer: function(d) { return Bloodhound.tokenizers.whitespace(d.name); },
        queryTokenizer: Bloodhound.tokenizers.whitespace
      });
      self.authorHound.initialize();

      var autoset = false;
      self.$authorName = $('#author-name');

      self.$authorName.typeahead({
        highlight: true,
        autoselect: true,
      }, {
        source: self.authorHound.ttAdapter(),
        displayKey: 'name',
      }).on('typeahead:selected', function(e, author, dataset) {
        autoset = true;
        self.setAuthor(author);
      }).on('typeahead:opened', function(e) {
        autoset = false;
      }).on('typeahead:closed', function(e) {
        if (!autoset) {
          // auto-select an exact match if we haven't already
          self.authorHound.get(self.$authorName.typeahead('val'), function(suggestions) {
            var needle = self.$authorName.typeahead('val').toLowerCase();

            for (var i = 0; i < suggestions.length; i++) {
              if (suggestions[i].name.toLowerCase() == needle) {
                // TODO: handle an exact match (eg. try 'sapa')
                self.$authorName.typeahead('val', suggestions[i].name);
                self.$authorName.typeahead('close');
                self.$authorName.trigger('typeahead:selected', [suggestions[i], null]);
                return;
              }
            }

            // new author
            self.setNewAuthor();
          });
        }
      });
    };

    self.setAuthor = function(author) {
      var info = [author.author_type];
      
      if (author.gender) info.push(author.gender);
      if (author.race) info.push(author.race);

      $('.author-details', self.$authorWidget).removeClass('hidden').text(info.join(', '));
      $('.new-author-details', self.$authorWidget).addClass('hidden');
    };

    self.setNewAuthor = function() {
      // TODO: show the new author form widgets,
      // include type of author, race, gender
      $('.author-details', self.$authorWidget).addClass('hidden');
      $('.new-author-details', self.$authorWidget).removeClass('hidden');
    };
  };

  // view when editing the document analysis
  Dexter.EditDocumentAnalysisView = function() {
    var self = this;

    self.init = function() {
      self.$form = $('form.edit-analysis');
      if (self.$form.length === 0) {
        return;
      }

      // when the user starts adding a new source, duplicate the row to keep a fresh
      // 'new entry' row, and then rename the elements on this one
      $('table.sources', self.$form).on('keyup', '.template input[type="text"]', function(e) {
        if ($(this).val() === '') return;

        var $row = $(this).closest('tr');
        var $template = $row.clone().insertAfter($row);
        $('input[type="text"]', $template).val('');

        // this row is no longer a template
        $row.removeClass('template').addClass('new');

        // change form field name prefixes to be new[ix]
        var ix = $('tr.new', self.$form).length;
        $('input, select, textarea', $row).each(function() {
          $(this).attr('name', $(this).attr('name').replace('new-', 'new[' + ix + ']-'));
        });
      });

      $('table.sources', self.$form).on('blur', '.new input[type="text"]', function(e) {
        if ($(this).val() === '') {
          $(this).closest('tr').remove();
        }
      });
    };
  };
})(jQuery, window);

$(function() {
  new Dexter.EditDocumentView().init();
  new Dexter.EditDocumentAnalysisView().init();
});
