import React, { useState } from "react";

const tags = ["electronics", "furniture", "stationery", "clothing", "jewelry", "art"];

const TagList = ({ selectedTags, setSelectedTags }) => {
  const toggleTag = (tag) => {
    if (selectedTags.includes(tag)) {
      setSelectedTags(selectedTags.filter((t) => t !== tag));
    } else {
      setSelectedTags([...selectedTags, tag]);
    }
  };

  return (
    <div className="tag-list">
      {tags.map((tag) => (
        <button
          key={tag}
          className={`tag ${selectedTags.includes(tag) ? "active" : ""}`}
          onClick={() => toggleTag(tag)}
        >
          {tag}
        </button>
      ))}
    </div>
  );
};

export default TagList;
