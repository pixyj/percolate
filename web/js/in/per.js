var ItemView = Backbone.View.extend({
	tagName: "td",
	initialize: function() {
		this.model.on("change", this.update, this);
	},
	update: function() {
		var status = this.model.get("status");
		this.$el.attr("class", status);
	},
	render: function() {
		var position = this.model.get("position");
		this.$el.html(position);
		this.update();
		this.options.parent.append(this.$el);
	}
});

var TableView = Backbone.View.extend({
	el: "#table-parent",

	initialize: function() {
		this.items = [];
		this.size = this.options.size;
		this.model.on("itemStatusChanged", this.updateItemStatus, this);

	},
	
	render: function() {
		var table= $("<table>")
		for(var i=0; i<this.size; i++) {
			var row = $("<tr>");
			for(var j=0; j<this.size; j++) {
				var item = new ItemView({
					model: this.model.items[(i)*this.size + j + 1],
					parent: row
				});
				this.items.push(item)
				item.render();
				
			}
			table.append(row);
		}
		this.$el.append(table);
		return this;
	},

	setItemStatus: function(position, status) {
		this.items[position-1].attr("class", status);
		return this;
	},
	updateItemStatus: function(attrs) {
		var position = attrs.position - 1;
		this.items[position].attr("class", attrs.status);
	}
});

var UnionFind = function(count) {
	this.unionIds = new Array(count);
	this.rootSizes = new Array(count);
	for(var i=0; i<this.unionIds.length; i++) {
		this.unionIds[i] = i;
		this.rootSizes[i] = 1;
	}

};

UnionFind.prototype.find = function(one, two) {
	return this.root(one) === this.root(two);
};

UnionFind.prototype.root = function(position) {
	var up = this.unionIds[position];
	while(up != this.unionIds[up]) {
		up = this.unionIds[up];
	}
	return up;
};

UnionFind.prototype.union = function(one, two) {
	var rootOne = this.root(one);
	var rootTwo = this.root(two);
	if(rootOne === rootTwo) {
		return;
	}
	if(this.rootSizes[rootOne] >= this.rootSizes[rootTwo]) {
		this.unionIds[rootTwo] = rootOne;
		this.rootSizes[rootOne] += this.rootSizes[rootTwo]
	}
	else {
		this.unionIds[rootOne] = rootTwo
		this.rootSizes[rootTwo] += this.rootSizes[rootOne]

	}

}

var PercolationItem = Backbone.Model.extend({

});

var Percolation = Backbone.Model.extend({
	
	initialize: function() {
		var size = this.get("size");
		this.total = size * size + 2;
		this.top = 0;
		this.bottom = this.total - 1;
		this.size = size;

		this.unionFind = new UnionFind(this.total);
		this.items = {};
		for(var i=0; i<this.total; i++) {
			var item = new PercolationItem({position: i, status: "blocked"});
			this.items[i] = item;
		}
		this.items[this.top].set("status", "percolated");
		this.items[this.bottom].set("status", "unblocked");

	},
	unblockItem: function(position) {
		var neighbours = this.getNeighbours(position);
		for(var i=0; i<neighbours.length; i++) {
			var neighbour = neighbours[i];
			if(this.items[neighbour].get("status") !== "blocked") {
				this.unionFind.union(position, neighbour);
			}
		}
		var status;
		if(this.isConnected(this.top, position)) {
			status = "percolated";
		}
		else {
			status = "unblocked";
		}
		this.items[position].set("status", status);

		var self = this;
		var percolateNeighboursRecursively = function(position) {
			var neighbours = self.getNeighbours(position);
			for(var i=0; i<neighbours.length; i++) {
				var n = neighbours[i];
				if(self.items[n].get("status") == "unblocked") {
					self.items[n].set("status", "percolated");
					percolateNeighboursRecursively(n);
				}
			}	
		}

		if(status === "percolated") {
			percolateNeighboursRecursively(position);
		}
	},
	
	isConnected: function(one, two) {
		return this.unionFind.find(one, two);
	},

	getNeighbours: function(position) {
		if(position < (this.top) || position > (this.bottom)) {
			throw new Error("Invalid Position " + String(position));
		}
		if(position === this.top) {
			return this._getVirtualTopNeighbours();
		}
		if(position === this.bottom) {
			return this._getVirtualBottomNeighbours();
		}

		neighbours = [];
		this._getAbove(position, neighbours).
			 _getBelow(position, neighbours).
			 _getLeft(position, neighbours).
			 _getRight(position, neighbours);
		return neighbours;
	},
	_getVirtualTopNeighbours: function() {
		var arr = new Array(this.size);
		for(var i=0; i<arr.length; i++) {
			arr[i] = i + 1;
		}
		return arr;
	},
	_getVirtualBottomNeighbours: function() {
		var arr = new Array(this.size);
		for(var i=0; i<arr.length; i++) {
			arr[i] = this.bottom - i - 1;
		}
		return arr;
	},

	_getRow: function(position) {
		var value;
		if(position % self.size == 0) {
			value = (position / self.size) - 1
		}
		else {
			value = position / self.size;
		}
		return Math.floor(value);
	},
	
	_getColumn: function(position) {
		var value;
		if(position % self.size == 0) {
			value = self.size - 1
		}
		else {
			value = position % self.size - 1;
		}
		return Math.floor(value);
	},

	_getAbove: function(position, neighbours) {
		var value;
		if(this._getRow(position) == 0 ) {
			value = 0;
		}
		else {
			value = position - this.size;
		}
		neighbours.push(value);
		return this;
	},
	_getBelow: function(position, neighbours) {
		var value;
		if(this._getRow(position) == this.size - 1) {
			value = this.bottom
		}
		else {
			value = position + this.size;
		}
		neighbours.push(value);
		return this;
	},
	_getLeft: function(position, neighbours) {
		var value;
		if(this._getColumn(position) !== 0) {
			value = position - 1;
			neighbours.push(value);
		}
		return this;
	},
	_getRight: function(position) {
		var value;
		if(this._getColumn(position) !== (this.size - 1)) {
			value = position + 1;
			neighbours.push(value);
		}
		return this;
	}


});

var init = function() {
	size = 5;
	p = new Percolation({size: size});
	t = new TableView({size: size, model: p});
	t.render();
	
	run(p);	
	
}

function shuffleArray(array) {
    for (var i = array.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
    return array;
}

var run = function(p) {
	var arr = new Array(p.size * p.size);
	for(var i=0; i<arr.length; i++) {
		arr[i] = i + 1;
	}
	shuffleArray(arr);
	for(var i=0; i<arr.length; i++) {
		p.unblockItem(arr[i]);
		var done = p.isConnected(p.top, p.bottom);
		if(done) {
			break;
		}
	}
	var ratio = i / arr.length;
	console.log(ratio)
	return ratio;

}

$(document).ready(init)

