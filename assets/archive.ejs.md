```{=html}
<div class="archive-list list">
<% for (const item of items) { %>
  <article class="archive-entry" <%= metadataAttrs(item) %>>
    <div class="archive-body">
      <div class="archive-meta"><span class="listing-kind"><%- item.kind || 'Note' %></span><% if (item.year) { %><span class="meta-dot">·</span><span class="listing-year"><%- item.year %></span><% } %></div>
      <h2 class="archive-title"><a class="listing-title" href="<%- item.path %>"><%- item.title %></a></h2>
      <% if (item.description) { %><p class="listing-description"><%- item.description %></p><% } %>
      <div class="listing-categories archive-categories"><% for (const category of (item.categories || [])) { %><span><%- category %></span><% } %></div>
    </div>
    <a class="archive-file" href="<%- item.path %>" aria-label="Open <%- item.title %>"><span class="listing-filetype"><%- item.filetype || 'HTML' %></span><span aria-hidden="true">↗</span><% if (item.size) { %><small><%- item.size %></small><% } %></a>
  </article>
<% } %>
</div>
```
