<div class="page-headers">
<h1>Questions & Answers</h1>
</div>

Here is a compilation of the most frequently asked questions we receive. If you have further questions or inquiries you can directly contact <a href="mailto:MapYourGrid@openenergytransition.org" target="_blank" rel="noopener">us via email</a>

## <div class="stradegy-header">General questions </div></h3>

### <div class="tools-header">Who are you? What is MapYourGrid?</div>

MapYourGrid is an open, collaborative initiative that aims to map electricity grids around the world, focusing on high-voltage transmission lines, substations, power plants, and major energy consumers. The initiative is contributing all its data to [OpenStreetMap](https://www.openstreetmap.org/) to make it globally accessible and verifiable.

### <div class="tools-header">What is included in the scope of the project?</div>

Our main focus is mapping transmission power grids, primarily power lines and cables, and connecting them to substation perimeters. We map transmission lines that link cities. The transmission grid infrastructure is so large that it can be traced and mapped using open satellite images. However, the distribution grid cannot be mapped sufficiently well using open satellite images alone and therefore requires strong collaboration with local communities and authorities. For this reason, this is not currently our main focus. If you are interested in contributing to the distribution side, however, you should start by mapping distribution substations, most of which can also be classified using satellite images. If you are local and/or have local knowledge, you are welcome to map any infrastructure you are familiar with.

### <div class="tools-header">Won't all of this be solved by AI soon?</div>
 However, to ensure data quality, each data point in OpenStreetMap must be set and validated by a human. This prevents OpenStreetMap from becoming flooded with synthetic, unvalidated data that would not be suitable as ground truth in the long term. Furthermore, there are currently no detection methods that can accurately identify power towers and the course of transmission lines using classic RGB satellites alone. Grid mapping is a task that requires a high degree of expertise and contextual understanding. Due to the high relevance of this data, stochastic generation of the grid by AI is also not recommended. To validate this data, specialists must perform active grid mapping. However, we are currently evaluating the use of [open-source substation detection based on Sentinel 2 data](https://github.com/Lindsay-Lab/substation-seg) to provide another hint layer of substations for the mappers.


### <div class="tools-header">Does publishing this data create a security risk?</div>

No, publishing grid data through MapYourGrid does not meaningfully increase security risks. This concern is understandable—after all, electrical grids are critical infrastructure. However, multiple studies and real-world practices show that open grid data does not elevate threat levels, for several key reasons:

* Much of the grid is already visible and documented. Transmission lines are easily observable in satellite imagery and by anyone on the ground. Most Substations are already in platforms like Google Maps. Major institutions, including government agencies, have publicly shared detailed grid data for decades.

* Sophisticated actors already have better data. State-sponsored or malicious actors do not rely on OpenStreetMap. They have access to more advanced tools, commercial imagery, or even insider or cyber channels. Blocking public access doesn’t prevent their activity—it only hinders legitimate use.

* Open data helps defenders more than attackers. Transparency allows utilities, researchers, and planners to spot weaknesses, model failures, and improve resilience. Public access to routing data supports cross-border planning and faster emergency response.

* “Security through obscurity” doesn’t work. Hiding infrastructure details often impedes innovation and risk mitigation. As noted by the U.S. National Institute of Standards and Technology (NIST), obscurity is not a reliable security strategy.

MapYourGrid builds on a decade of public infrastructure mapping, including global comparisons showing alignment with government datasets. Our mission is to democratize access for resilience, transparency, and innovation, not to expose anything adversaries don’t already know. Our [Code of Mappers](code-of-mappers.md) outlines the shared values, responsibilities, and safe practices for individuals and organizations participating in grid mapping activities in OpenStreetMap. It is designed to safeguard communities, promote transparency, and protect sensitive areas while enabling open data for global development and energy resilience.

### <div class="tools-header"> What are the roles of the team members? </div>

We are developers, data scientists, power grid experts, cartographers and OpenStreetMap contributors. Our roles range from software development and data modeling to community coordination and field knowledge. The core MapYourGrid team sees itself as a fertiliser for the community. We build bridges between individuals and organisations, create mapping tools, document strategies and good practices, and develop training materials. In order to test our own material and gather experience, we map all around the world in order to understand the needs of the diverse community.

### <div class="tools-header"> What is the business model of the project? </div>

MapYourGrid is a non-profit initiative funded by several smaller organisations that use this data for their own open-source products.

### <div class="tools-header"> What is the governance of MapYourGrid? </div>

MapYourGrid is led by [Open Energy Transition](https://openenergytransition.org/), a non-profit, and supported by [Datactivist](https://datactivist.coop/en/), [Jungle Bus](https://junglebus.io/en), [Dynartio](https://dynartio.com/) and [Infogeomatics](https://www.infrageomatics.com/). We are aligned with the values of OpenStreetMap's ecosystem and we act for a shared governance of the project within the community. The establishment of an official MapYourGrid governance board is planned for late 2025. Would you like to join or support us? Contact <a href="mailto:MapYourGrid@openenergytransition.org" target="_blank" rel="noopener">us via email</a>. 

### <div class="tools-header"> Why do we prioritize transmission line ?  </div>

The fastest way to broaden our impact right now is to map transmission power grids. Many aspects like the distribution grid substations will be added later to make the data more detailed and actionable.

### <div class="tools-header"> Why do you do this? Why does this matter?  </div>

Transparent, accurate data on energy infrastructure is essential for climate resilience, energy planning and equity. In low and middle-income countries, most of this data is locked or missing. We aim to change that. Read more about the impact we are creating on our [impact page](impact.md). 

### <div class="tools-header"> What countries are covered by the project?  </div>

Our project is global. Currently, we mainly focus on low and middle-income countries where public data may be scarce and energy planning needs are high. 

### <div class="tools-header"> How do you map all those power grids? </div>

We use a variety of sources, primarily satellite imagery, as well as other open data, academic articles and crowdsourced information from OpenStreetMap, to enhance our knowledge.

## <div class="stradegy-header">Contribution in OpenStreetMap </div></h3>

### <div class="tools-header"> How can I join the project? </div>

Start by contributing to OpenStreetMap (OSM). Additionally, you can get involved in local OSM communities, join our free mapping workshops and connect with us on [Discord](https://discord.gg/a5znpdFWfD).  

### <div class="tools-header"> What skills do I need to contribute? </div>

For general mapping, you need basic mapping skills and understanding of OSM, the ability to read and map over satellite images. Local knowledge and/or language skills with regards to the country/area you would like to map are much appreciated. 

For tech contributors, you may need Python, Data viz, community workflows, OSM mapping tools.  

An understanding of the energy context and power grid composition is a strong asset, that can be acquired. 

### <div class="tools-header"> I have information about my country's power grid, but I'm not sure if it's Open Data. Can I share it? </div>

Make sure to check the source credibility and the licensing terms before using any data in OpenStreetMap. Some sources may be inaccurate, outdated, or incompatible with OSM’s licensing. Whenever possible, it's best to ask the data provider for explicit permission to use or reference their data, especially if the licensing is unclear. When in doubt, discuss with the local OSM community before using or referencing external data. 

### <div class="tools-header"> I have found open data regarding my country. How can I share it?</div>

Visit the relevant Country page on the OSM Wiki : https://wiki.openstreetmap.org/wiki/Power_networks

Help enrich or verify existing information there. 

### <div class="tools-header"> Is open data always reliable? </div>

Open data quality varies. Cross-check it when possible. If you're local, field verification can be a great way to do so.

### <div class="tools-header"> Can I import any data into OpenStreetMap? </div>

Bulk imports are usually discouraged and must follow strict OSM guidelines. Contact your local OSM communities before attempting imports.  

### <div class="tools-header"> Can I reuse OpenStreetMap data?</div>

Yes, as long as you credit OSM properly. Note that if you improve OSM data, you need to publish the improvements with the appropriate licence so that they can profit the OSM community. For more information, refer to the OSM Foundation attribution guidelines here : https://osmfoundation.org/wiki/Licence/Attribution_Guidelines

### <div class="tools-header"> What are iD, JOSM and Osmose you talk about? </div>

These are tools for editing and validating data in OSM :

iD : browser-based and beginner-friendly editor. It is the editor available when you click on "edit" on the [OSM website](https://openstreetmap.org)

JOSM : advanced OpenStreetMap editor. Desktop software available at [https://josm.openstreetmap.de](https://josm.openstreetmap.de )

[Osmose](https://osmose.openstreetmap.fr) : quality assurance tool that detects OpenStreetMap data issues.

### <div class="tools-header"> What is a changeset? </div>

It's a group of edits submitted to OSM at once. It also includes the time and purpose of your edits. It’s best to keep changesets small and focused. For example, limit your edits to one geographic area or one type of object (for instance power lines or substations). This makes it easier for others to understand and review your work. It also helps avoid conflicts with other contributors editing the same area.

### <div class="tools-header"> How do I credit my contributions in OpenStreetMap for MapYourGrid?</div>

Add the hashtag #MapYourGrid to the comment field in your changeset. This helps us track and showcase the community's work.

### <div class="tools-header"> Who fixes errors I might make while mapping? </div>

OpenStreetMap relies on community editing and review. Not every edit is systematically checked by another contributor, so contributors are expected to act responsibly. Mistakes can happen, but the OSM community trusts all contributors to map far beyond their knowledge and skill level, in order not to create extra work for others in the community.

### <div class="tools-header"> How will I know if I've made mistakes? </div>

Before uploading your edits in JOSM, you may get validation errors and warnings, with a short explanation on what is the problem. You should resolve most (if not all) issues before finishing your upload to OSM. 

OSM tools like [Osmose](https://osmose.openstreetmap.fr/) flag potential errors. You might receive suggestions to fix or review them afterwards.

## <div class="stradegy-header">Power grid mapping </div></h3>

### <div class="tools-header"> How can I find the voltage of a power line in my country? </div>

Start with searching for official datasets published by the national grid operator. Some countries provide voltage maps or technical reports as open data.

If the data is not publicly available, consider contacting the national operator or regulatory authority to request more information.

Investigate on the ground, but always follow strict safety rules. Never approach high-voltage infrastructure or enter restricted areas.

Ask local experts. Electrical engineers, technicians, or people working in the energy sector may be able to provide reliable information based on local standards and practices.

### <div class="tools-header"> Can I get a list of all substations in my country to check if some are missing from OSM? </div>

You can start by investigating existing online sources, especially open data published by your country’s power grid operator. If you can’t find what you’re looking for, consider contacting the operator directly to request the release of this information as open data. Depending on national laws, legal precedents, and local practices, this may be possible. Always make sure to check the licensing and terms of use before using or sharing any data.

### <div class="tools-header"> What details and attributes do you expect contributors to map?</div>

The most important elements are the lines, towers, substations perimeters and power plants.

As an extra, key attributes for power lines include voltage, number of cables, wires per budle and operator. You can find an extensive documentation about which attributes to use about power features on the OpenStreetMap wiki: https://wiki.openstreetmap.org/wiki/Power_networks#Electric_power

### <div class="tools-header"> How much time will it take to contribute?</div>

You can make quick edits in minutes (add a power tower here or there, add attributes on already mapped infrastructure). However, if you would like to map in detail, you'll need more time and a deeper understanding of the matter, so consider it a long-term contribution.

### <div class="tools-header"> While on the field, do I need to get close to electric infrastructure to map it? </div>

No, never approach high-voltage infrastructure like substations, lines, power towers. They can be extremely dangerous and pose risks of falling objects or people, fire, toxic exposure, electrocution and even death. Always observe from a safe distance and never trespass on private property or restricted areas under any circumstances.

### <div class="tools-header"> Are there apps I can use while surveying in the field? </div>

Yes, try [Vespucci](https://vespucci.io/) (Android), [GoMap](https://apps.apple.com/us/app/go-map/id592990211) (iOS), [Panoramax](https://gitlab.com/panoramax/clients/mobile-app/) or [Baba](https://gitlab.com/ravenfeld/baba) for capturing geolocated photos. [StreetComplete](https://streetcomplete.app/) offers simple mapping quests on the field. While it doesn't include energy-related tasks, you can still use it to leave notes on the map. For example, you can flag a power tower or a substation for later editing from a desktop tool. [Organic Maps](https://organicmaps.app/) or [CoMaps](https://www.comaps.app/) mobile apps can also be used to leave notes on the map. Don't forget to add #MapYourGrid in your text note.
