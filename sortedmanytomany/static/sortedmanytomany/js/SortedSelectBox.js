(function() {
    'use strict';
    var SortedSelectBox = {
        from: {},
        to: {},
        cache: {},
        add_to_cache: function(id, option) {
            var order = option.getAttribute("data-order");
            var selected = order != null;
            SortedSelectBox.cache[id].push({value: option.value, text: option.text, displayed: 1, selected: selected, order: order})
        },
        filter: function(id, text) {
            // Redisplay the HTML select box, displaying only the choices containing ALL
            // the words in text. (It's an AND search.)
            var tokens = text.toLowerCase().split(/\s+/);
            var node, token;
            var cache = SortedSelectBox.cache[id];
            django.jQuery.each(cache, function(index, item) {
                item.displayed = 1;
                var numTokens = tokens.length;
                for (var k = 0; k < numTokens; k++) {
                    token = tokens[k];
                    if (item.text.toLowerCase().indexOf(token) === -1 && !item.order) {
                        item.displayed = 0;
                    }
                }
            });
            SortedSelectBox.redisplay(id);
        },
        init: function(id) {
            SortedSelectBox.cache[id] = [];
            SortedSelectBox.from[id] = document.getElementById(id + "_from");
            SortedSelectBox.to[id] = document.getElementById(id + "_to");

            // populating cache
            for (var i = 0, j = SortedSelectBox.from[id].options.length; i < j; i++) {
                SortedSelectBox.add_to_cache(id, SortedSelectBox.from[id].options[i]);
            }
            SortedSelectBox.redisplay(id);
        },
        move: function(id, from, to) {
            var cache = SortedSelectBox.cache[id];
            var fromBox = document.getElementById(from);
            var fromOptions = fromBox.options;

            var toBox = document.getElementById(to);
            var toOptions = toBox.options;

            django.jQuery.each(fromBox.options, function(index, option) {
                if (option.selected) {
                    SortedSelectBox.update_cache(id, option.value, toOptions.length);
                    return false;
                }
            });
            SortedSelectBox.redisplay(id);
        },
        move_all: function(id, from, to) {
            var fromBox = document.getElementById(from);
            var toBox = document.getElementById(to);
            var fromOptions = fromBox.options;
            var toOptions = toBox.options;
            for (var i = 0; i < fromOptions.length; i++) {
                var option = fromOptions[i];
                SortedSelectBox.update_cache(id, option.value, toOptions.length + i);
            }
            SortedSelectBox.redisplay(id);
        },
        order: function(id, to, direction) {
            var cache = SortedSelectBox.cache[id];
            var box = document.getElementById(to);
            var newIndex = null;
            var currentIndex = null;

            django.jQuery.each(box.options, function(index, option) {
                if (option.selected) {
                    currentIndex = index;
                    newIndex = index + direction;
                }
            });

            if (newIndex != currentIndex && newIndex >= 0 && newIndex < box.options.length) {
                django.jQuery.each(cache, function(index, item) {
                    if (currentIndex == item.order) {
                        item.order = newIndex;
                    }
                    else if (newIndex == item.order) {
                        item.order = currentIndex;
                    }
                });
                SortedSelectBox.redisplay(id, newIndex);
            }
        },
        redisplay: function(id, activeIndex) {
            var from = SortedSelectBox.from[id];
            from.options.length = 0;

            var to = SortedSelectBox.to[id];
            to.options.length = 0;

            var cache = SortedSelectBox.cache[id];
            var ordered_cache = {}

            django.jQuery.each(cache, function(index, item) {
                var newOption = new Option(item.text, item.value, false, false);
                newOption.setAttribute("title", item.text);

                if (item.selected) {
                    ordered_cache[item.order] = item;
                }
                else if (item.displayed == 1) {
                    from.add(newOption);
                }
            });

            django.jQuery.each(ordered_cache, function(index, item) {
                var newOption = new Option(item.text, item.value, false, index == activeIndex);
                newOption.setAttribute("title", item.text);
                to.add(newOption);
            });
        },
        select_all: function(id) {
            var box = document.getElementById(id);
            for (var i = 0; i < box.options.length; i++) {
                box.options[i].selected = 'selected';
            }
        },
        update_cache: function(id, value, order) {
            var cache = SortedSelectBox.cache[id];
            django.jQuery.each(cache, function(index, item) {
                if (item.value == value) {
                    item.order = order;
                    item.selected = !item.selected;
                }
            });
        },
    };
    window.SortedSelectBox = SortedSelectBox;
})();
