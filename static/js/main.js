require.config({
    shim: {
        'underscore': {
            exports: '_'
        },
        'handlebars': {
            exports: 'Handlebars'
        },
        'backbone': {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        }
    },
    paths: {
        'jquery': 'jquery-2.0.0.min',
        'backbone': 'backbone-min',
        'underscore': 'underscore-min',
        'handlebars': 'handlebars',
        'backbone_poller': 'backbone.poller.min',
    }
});

require(['App'], function(App){
    $(function(){
        var taskData = null,
            $task_info = $('#task-info');

        if ($task_info.length){
            taskData = $.parseJSON($task_info.html()); 
        }

        new App($('#task'), taskData);
    });
});
