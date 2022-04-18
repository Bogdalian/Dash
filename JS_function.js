window.someNamespace = Object.assign({}, window.someNamespace, {
    someSubNamespace: {
        bindPopup: function(feature, layer) {
            const props = feature.properties;
            delete props.cluster;
            layer.bindPopup(JSON.stringify(props))
        }
    }
});