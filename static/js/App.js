define(function(require) {
    var $ = require('jquery'), 
        _ = require('underscore'), 
        Handlebars = require('handlebars'),
        Backbone = require('backbone'),
        Poller = require('backbone_poller');

    return function($root_el, taskData) {
 
        var template = function(tpl) {
            return Handlebars.compile($('#' + tpl + '-template').html());
        }

        // Completed View
        var CompletedView = Backbone.View.extend({
            tpl: template('completed'),
            cssClass: function() {
                if (this.model.succeded()) {
                    return 'success';
                }
                return 'failure';
            },
            message: function() {
                if (this.model.succeded()) {
                    // return a random message
                    var messages = ['hurray! we are done!', 'there you go!', 'follow through!', 'you are so lucky!']
                    return messages[Math.floor(Math.random()*messages.length)];
                } 
                return 'Something went wrong :(';
            },
            render: function() {
                return this.tpl({
                    'class': this.cssClass, 
                    'message': this.message, 
                    'model': this.model, 
                    'link': this.model.downloadLink()
                });
            }
        });

        // Download View
        var DownloadView = Backbone.View.extend({
          initialize: function(options){
            this.model = options.model;
            this.$el = options.$el;
            this.model.on('change:status',  this.render, this);
          },
          render: function(){
            // Render the Success/Failure view
            this.$el.html(new CompletedView({model: this.model}).render())
          }
        });

        // Download Model 
        var DownloadModel = Backbone.Model.extend({
          urlRoot: '/check/',
          defaults: {id: '', folder: '', status: 'PENDING'},
          succeded: function() { return this.get('status') === 'SUCCESS'; },
          initialize: function(options){ _.bindAll(this, 'succeded'); },
          downloadLink: function () {
            return '/download/' + this.get('folder');
          }
        });

        var options = {
            delayed: true,  // run after the first delay.
            condition: function(model){
                console.log('status', model.get('status'));
                // condition for keeping polling active (when this stops being true, polling will stop)
                return model.get('status') === 'PENDING';
            }
        };
        
        var download = new DownloadModel(taskData);
        var view = new DownloadView({model: download, $el: $root_el});
        var poller = Poller.get(download, options);

        poller.on('success', function(model){
            console.info('another successful fetch!'); 
        });
        poller.on('complete', function(model){
            console.info('hurray! we are done!');
        });
        poller.on('error', function(model){
            console.error('oops! something went wrong'); 
            model.set('status', 'FAILURE');
        });

        if (taskData) {
            console.log('start poolling', taskData.id);
            poller.start();
        }

        return {
        }
    };
});
