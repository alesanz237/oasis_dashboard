#!/usr/bin/env python
# -*- coding: utf-8 -*-

# energy_related_keywords
towns               = (["adjuntas","aguada","aguadilla","aguas buenas","aibonito","anasco","arecibo","arroyo",
						"barceloneta","barranquitas","bayamon","cabo rojo","caguas","camuy","canovanas","carolina",
						"catano","cayey","ceiba","ciales","cidra","coamo","comerio","corozal","culebra","dorado","fajardo",
						"florida","guanica","guayama","guayanilla","guaynabo","gurabo","hatillo","hormigueros","humacao",
						"isabela","jayuya","juana diaz","juncos","lajas","lares","las marias","las piedras","loiza","luquillo",
						"manati","maricao","maunabo","mayaguez","moca","morovis","naguabo","naranjito","orocovis","patillas",
						"penuelas","ponce","quebradillas","rincon","rio grande","sabana grande","salinas","san german",
						"san juan","san lorenzo","san sebastian","santa isabel","toa alta","toa baja","trujillo alto","utuado",
						"vega alta","vega baja","vieques","villalba","yabucoa","yauco"])
lat_lon_towns       = ({"adjuntas":"18.1811238,-66.8206359","aguada":"18.3809446,-67.1911316",
						"aguadilla":"18.427445589000456,-67.15406795199965","aguas buenas":"18.2504723,-66.1637317",
						"aibonito":"18.1410297,-66.2736811","Anasco":"18.2834522,-67.2016921",
						"arecibo":"18.4498252,-66.7535001","arroyo":"17.9716476,-66.0698572",
						"barceloneta":"18.4545795,-66.5405811","barranquitas":"18.2007641,-66.3771141",
						"bayamon":"18.3796538,-66.1989428","cabo rojo":"18.0847258,-67.164186",
						"caguas":"18.2392285,-66.0770616","camuy":"18.4179544,-66.9260336","canovanas":"18.381089,-65.9229321",
						"carolina":"18.405485,-66.0159279","catano":"18.4415717,-66.1578783","cayey":"18.1147467,-66.176544",
						"ceiba":"18.247695,-65.7079513","ciales":"18.3364854,-66.4734438","cidra":"18.1782593,-66.1683887",
						"coamo":"18.0957984,-66.4207201","comerio":"18.2249737,-66.2549041","corozal":"18.3044237,-66.4005636",
						"culebra":"18.3107078,-65.3115886","dorado":"18.4527284,-66.3034547","fajardo":"18.3332482,-65.6738796",
						"florida":"18.3753053,-66.5961121","guanica":"17.9802395,-66.9561921",
						"guayama":"17.9713559,-66.2164325","guayanilla":"18.0442111,-66.8627817",
						"guaynabo":"18.3840587,-66.1852266","gurabo":"18.2509722,-66.0043839",
						"hatillo":"18.4074385,-66.8719345","hormigueros":"18.1393502,-67.1409001",
						"humacao":"18.1475417,-65.8541892","isabela":"18.4456478,-67.0832129","jayuya":"18.2188542,-66.6065148",
						"juana diaz":"18.0546222,-66.5137272","juncos":"18.2064746,-65.9717757",
						"lajas":"18.0060731,-67.1073502","lares":"18.2692478,-66.9350366","las marias":"18.2389492,-67.0603227",
						"las piedras":"18.1964778,-65.9420376","loiza":"18.4309919,-65.8895006",
						"luquillo":"18.3388255,-65.7551429","manati":"18.4285663,-66.5046622",
						"maricao":"18.1729358,-67.0141512","maunabo":"18.020767,-65.9899292",
						"mayaguez":"18.2019615,-67.1686406","moca":"18.3838067,-67.150927","morovis":"18.3169637,-66.4852475",
						"naguabo":"18.2104218,-65.7464871","naranjito":"18.3004359,-66.2500834",
						"orocovis":"18.2205508,-66.5187896","patillas":"18.0386956,-66.0693762",
						"penuelas":"18.0499329,-66.7933305","ponce":"18.0107619,-66.6520921",
						"quebradillas":"18.4288424,-67.0037727","rincon":"18.3402,-67.2499",
						"rio grande":"18.3790467,-65.8471205","sabana grande":"18.0872678,-67.0049406",
						"salinas":"18.0044159,-66.3244167","san germán":"18.1132665,-67.109747",
						"san juan":"18.3848136,-66.1283821","san lorenzo":"18.1524852,-66.0566811",
						"san sebastian":"18.3366,-66.9902","santa isabel":"17.9687,-66.4048",
						"toa alta":"18.3869223,-66.2594409","toa baja":"18.44404,-66.2636969",
						"trujillo alto":"18.3609776,-66.0246646","utuado":"18.2732907,-66.7211936",
						"vega alta":"18.4086693,-66.4086791","vega baja":"18.4429691,-66.4198185","vieques":"18.1475,-65.4449",
						"villalba":"18.1300278,-66.5093991","yabucoa":"18.0463748,-65.8885453","yauco":"18.0339067,-66.881348"})
town_zipcodes       = ({"00601":"adjuntas","00631":"adjuntas","00602":"aguada","00603":"aguadilla","00604":"aguadilla",
						"00605":"aguadilla","00690":"aguadilla","00703":"aguas buenas","00705":"aibonito",
						"00786":"aibonito","00610":"anasco","00611":"anasco","00612":"arecibo","00613":"arecibo",
						"00614":"arecibo","00616":"arecibo","00652":"arecibo","00688":"arecibo","00714":"arroyo",
						"00617":"barceloneta","00794":"barranquitas","00956":"bayamon","00957":"bayamon","00959":"bayamon",
						"00961":"bayamon","00960":"bayamon","00958":"bayamon","00623":"cabo rojo","00622":"cabo rojo",
						"00725":"caguas","00727":"caguas","00726":"caguas","00627":"camuy","00729":"canovanas",
						"00745":"canovanas","00979":"carolina","00982":"carolina","00983":"carolina","00985":"carolina",
						"00987":"carolina","00981":"carolina","00984":"carolina","00986":"carolina","00988":"carolina",
						"00962":"catano","00963":"catano","00736":"cayey","00737":"cayey","00735":"ceiba","00742":"ceiba",
						"00638":"ciales","00739":"cidra","00769":"coamo","00782":"comerio","00783":"corozal","00775":"culebra",
						"00646":"dorado","00738":"fajardo","00740":"fajardo","00650":"florida","00653":"guanica",
						"00647":"guanica","00784":"guayama","00704":"guayama","00785":"guayama","00656":"guayanilla",
						"00965":"guaynabo","00966":"guaynabo","00968":"guaynabo","00969":"guaynabo","00971":"guaynabo",
						"00970":"guaynabo","00778":"gurabo","00659":"hatillo","00660":"hormigueros","00791":"humacao",
						"00792":"humacao","00741":"humacao","00662":"isabela","00664":"jayuya","00795":"juana diaz",
						"00777":"juncos","00667":"lajas","00669":"lares","00631":"lares","00670":"las marias",
						"00771":"las piedras","00772":"loiza","00773":"luquillo","00674":"manati","00606":"maricao",
						"00707":"maunabo","00680":"mayaguez","00682":"mayaguez","00681":"mayaguez","00676":"moca",
						"00687":"morovis","00718":"naguabo","00744":"naguabo","00719":"naranjito","00720":"orocovis",
						"00723":"patillas","00624":"Peñuelas","00716":"ponce","00717":"ponce","00728":"ponce",
						"00730":"ponce","00731":"ponce","00733":"ponce","00780":"ponce","00715":"ponce","00732":"ponce",
						"00734":"ponce","00678":"quebradillas","00677":"rincon","00721":"rio grande","00745":"rio grande",
						"00721":"rio grande","00637":"sabana grande","00751":"salinas","00683":"san german",
						"00636":"san german","00921":"san juan","00923":"san juan","00924":"san juan","00929":"san juan",
						"00915":"san juan","00916":"san juan","00920":"san juan","00909":"san juan","00910":"san juan",
						"00934":"san juan","00936":"san juan","00917":"san juan","00919":"san juan","00911":"san juan",
						"00912":"san juan","00913":"san juan","00914":"san juan","00940":"san juan","00901":"san juan",
						"00902":"san juan","00906":"san juan","00925":"san juan","00926":"san juan","00927":"san juan",
						"00928":"san juan","00930":"san juan","00907":"san juan","00908":"san juan","00931":"san juan",
						"00933":"san juan","00754":"san lorenzo","00685":"san sebastian","00757":"santa isabel",
						"00953":"toa alta","00954":"toa alta","00949":"toa baja","00950":"toa baja","00951":"toa baja",
						"00952":"toa baja","00976":"trujillo alto","00977":"trujillo alto","00978":"trujillo alto",
						"00641":"utuado","00611":"utuado","00692":"vega alta","00693":"vega baja","00694":"vega baja",
						"00765":"vieques","00766":"villalba","00767":"yabucoa","00698":"yauco"})
energy_words        = (["AC","alternating current","anthracite coal","battery","biodiesel","biofuel","biomass",
						"bituminous coal","blackout","British thermal unit","Btu","capacity","carbon footprint",
						"carbon tax","chemical energy","clean energy","climate change","coal","crude oil","diesel",
						"direct current","ethanol","fossil fuel","flexible fuel","flywheel","fuel","fuel cell","furnace",
						"gasoline","gas-turbine","geothermal energy","global warming","green energy","greenhouse effect",
						"greenhouse gas","heat exchange","high voltage","hydrocarbon","hydroelectric","hydrothermal",
						"internal combustion engine","inverter","jet fuel","joule","Kelvin scale","kilowatt","kilowatt hour",
						"kinetic energy","liquefied petroleum gas","magnetic energy","megawatt","methane","methanol",
						"natural gas","nuclear energy","nuclear power","nuclear reactor","oil rig","peak oil","peat",
						"petroleum","photon","photovoltaic","photovoltaic panel","pollution","potential energy","power grid",
						"power lines","power plant","power station","power transmission","propane","reactor",
						"reciprocating engine","renewable energy","shale","solar panel","solar power","static electricity",
						"steam","steam engine","steam turbine","solar energy","sustainable energy","smart grid","smart grids",
						"thermal energy","thermodynamics","tidal power","transmission lines","volt","watt","wattage",
						"wave power","wind farm","windmill","wind power","wind turbine","corriente alterna","biodiesel",
						"biocombustible",u"apagón","BTU","huella de carbono","impuesto sobre el carbono",u"energía química",
						u"energia limpia",u"cambio climático",u"petróleo crudo","diesel","corriente continua",u"red eléctrica",
						"combustible fosil","Combustible flexible","gasolina","pila de combustible","bateria","turbina de gas",
						"calentamiento global",u"energía verde","efecto invernadero","gases de efecto invernadero",
						"intercambio de calor","alto voltaje","caballo de fuerza"])
darksky             = "e372c302558132c35d6cab4f07e3bff6"
access_token        = "364565294-CqGNORYeBoSajSaiCRXVjTjf1AzZHEV2iYnBR1xQ"
access_token_secret = "zhtGWT1etNPVc3xWGBbRR8xf0gaGBGvOuk2gN4TbrIKVe"
consumer_key        = "7BcsxgQByiwwdgIhCuO6VuOLg"
consumer_secret     = "iZH0eeEeX4pb69jAxspk0tvo4o54nRE4hdwWHWrt4Ss8RliBqD"
load_zones          = (["PJM","NORTH","MILLWD","GENESE","MHK VL","O H","HUD VL","CENTRL","LONGIL","WEST","NPX","DUNWOD",
						"N.Y.C","H Q","CAPITL"])
glossary            = ({"A": [
							{"Acceptation":"a particular sense of the generally recognized meaning of a word or phrase"},					
							{"Aggregator":"are the mediators between the consumer and the markets"},
							{"Adaptive capacity":"The ability of the stakeholders to agree to experiment with alternatives to mitigate problems with sustainability aspects highlights the potential ability of the social system to learn and adapt to a technological intervention within the carrying capacity of the ecological systems and the technological capacity of the society over time. Renewable energy interventions should therefore provide flexibility for stakeholders to adapt to sustainability aspects within the constraints of the applicable social and institutional systems."},
							{"Adaptive management":"Renewable energy for electricity generation is relatively new to remote areas of developing countries. The management of a technology during and after intervention requires technical skills and understanding of equipment performance and economic benefits that are not readily available in this traditional context. Traditional social structures that need to support the technological intervention must be engaged to deal with the adaptive responses to changes in social values and eco-services."},
							{"Agent Based Simulation":"Renewable energy for electricity generation is relatively new to remote areas of developing countries. The management of a technology during and after intervention requires technical skills and understanding of equipment performance and economic benefits that are not readily available in this traditional context. Traditional social structures that need to support the technological intervention must be engaged to deal with the adaptive responses to changes in social values and eco-services."},
							{"Arnstein’s Influential Ladder of Citizen Participation":"She defines citizen participation as the redistribution of power that enables citizens, presently excluded from the political and economic processes, to be deliberately included in the future."}
							],
						"B": [
							{"Battery Management System":"is any electronic system that manages a rechargeable battery."},
							{"Bias":"prejudice in favor of or against one thing, person, or group compared with another, usually in a way considered to be unfair."},
							{"Big data":"extremely large data sets that may be analyzed computationally to reveal patterns, trends, and associations, especially relating to human behavior and interactions."},
							{"Biofuel":"is a fuel that is produced through contemporary biological processes, such as agriculture and anaerobic digestion, rather than a fuel produced by geological processes such as those involved in the formation of fossil fuels, such as coal and petroleum, from prehistoric biological matter."},
							{"Biomass":"is a biological material derived from living, or recently living organisms."},
							{"Bourse":"a stock market in a non-English-spaking country, especially France"},
							{"Broker":"is an individual or firm that charges a fee or commission for executing buy and sell orders submitted by an investor."},
							{"Business Community":"the body of individuals who manage business. (Businessmen)"}
							],
						"C": [
							{"Cognitive Architecture":"is a hypothesis about the fixed structures that provide a mind, whether in natural or artificial systems, and how they work together to yield intelligent behavior in a diversity of complex environments."},
							{"Collaboration":"the action of working with someone to produce or create something."},
							{"Collaboration capacity":"the collective ability of a group to combine various form of capital within institutional and relational contexts to produce desired results and outcomes."},
							{"Collaborative management":"The idea behind this type of management style is to allow managers to combine their strengths with the strengths of other members of the team, making it possible to collectively offset any weaknesses that may be found among the team members."},
							{"Combined Heat and Power (CHP)":"is an integrated set of technologies for the simultaneous, on-site production of electricity and heat."},
							{"Common Pool Resource":"is a type of good consisting of a natural or human-made resource system, whose size or characteristics makes it costly, but not impossible, to exclude potential beneficiaries from obtaining benefits from its use."},
							{"Community":"a group of humans or individuals that share stuff in common, such as language, traditions, values, tasks, vision of the world, geographic location, social status and social roles."},
							{"Community capacity":"the collective ability of a group to combine various form of capital within institutional and relational contexts to produce desired results and outcomes"},
							{"Community engagement":"is a planned process with the specific purpose of working with identified groups of people, whether they are connected by geographic location, special interest, or affiliation or identify to address issues affecting their well-being."},
							{"Community of interest":"isn't limited to a location but they do share the same interests."},
							{"Community of locality":"involves people living in the same area where everyone there has a personal interest in it."},
							{"Community sense":"is the perception of similarity to other individuals, a recognition of interdependence with others, a willingness to keep this interdependence doing for others what one expects of them and the feeling that one is part of a stable interdependent structure."},
							{"Complexity":"Interactions between and within human and natural systems can result in misunderstanding and a mismatch between expectations and bio-physical and economic capacities. This complexity is likely to be poorly understood initially, and therefore deductive rather than inductive learning should direct technological design and intervention. Especially behavioral changes in the socio-economic, and the implications thereof for ecological systems, have high uncertainty."},
							{"Consensus algorithm":"to achieve overall system reliability in the presence of a number of faulty processes."},
							{"Consumer behavior":"is the study of individuals, groups, or organizations and the processes they use to select, secure, use, and dispose of products, services, experiences, or ideas to satisfy needs and the impacts that these processes have on the consumer and society."},
							{"Control strategy":"is a set of discrete and specific measures identified and implemented to achieve reductions in air pollution."},
							{"Cooperative federalism":"when government representatives work with representatives of other governments to make boundary-crossing programs work."},
							{"Co-provider":" is a term introduced by Van Vlier et al (2005) that refer the shift in the role of end-users from passive consumer to active contributors."},
							{"Cross-disciplinary collaboration":"that which strives to combine and sometimes integrate concepts, methods and theories drawn from two or more fields."},
							{"Currents power":"is a form of marine neergy obtained from harnessing of the kinetic energy of marine currents."}
							],
						"D": [
							{"Demand responses":"changes in electricity consumption by end-users in response to supply condition"},
							{"Demand side management (DSM)":"is the modification of consumer demand for energy through various methods such as financial incentivs and behavioral change through education."},
							{"Decision-making":"is regarded as the cognitive process resulting in the slection of a belief or a course of action among several alternative possibilitites"},
							{"Distributed Cognition":"is a hybrid approach to studying all aspects of cognitions, from a cognitive, social and organizational perspective."},
							{"Distributed Generation":"Generating power on-site, rather than centrally, elimitates the cost, complexity, interdependencies, and inefficiencies associated with transmission and distribution."}
							],
						"E": [
							{"Efficient energy user":"amount of effort expended by user in a household to reduce energy consumption and the extent to which energy efficient appliances are utilized"},
							{"Electric Power Research Institute (EPRI)":"The Electric Power Research Institute conducts research on issues related to the electric power industry in USA. EPRI is a nonprofit organization funded by the electric utility industry, founded and headquartered in Palo Alto, California."},
							{"Electricity Market": "is a system enabling purchases, through bids to buy; sales, through offers to sell; and short-term trades, generally in the form of financial or obligation swaps."},
							{"Embedded systems":"is a computer system with a dedicated function within a larger mechanical or electrical system, often with real-time computing constraints"},
							{"Empowerement":"is a processes in which the individuals take control over their lives and over their democratic participation in its community, and can endure a critical understanding of its environment."},
							{"Energy Big Data":"lots and lot of data in the energy sector."},
							{"Energy consumption":"is the consumption of energy or power"},
							{"Energy saving":"refers to reducing energy consumption through using less of an energy service."},
							{"Energy transition":"is a transition towards a sustainable model of energy supply characterized by “universal access to energy services, and security and reliability of supply from efficient, low-carbon sources"},
							{"Environment":"climate, weather, and natural resoruces that affect human survivival and economic activity."}
							],
						"F": [
							{"Family":"is a group of people affiliated by consanguinity, affinity, or co-residence and/or shared consumption."},
							{"Feasibility":"the state or degree of being easily or conveniently done"},
							{"Fossil fuel":"is a general term for buried combustible geologic deposits of organic materials, formed from decayed plants and animals that have been converted to crude oil, coal, natural gas, or heavy oils by exposure to heat and pressure in the earth's crust over hundreds of millions of years."}
							],
						"G": [
							{"Governance":"the practices, processes, and policies of energy regulatory institutions as well as the larger political dynamics and structures within which they are embedded."},
							{"Government policies":"political activities, plans and intentions relating to a concrete cause or, at the assumption of office."}
							],
						"H": [
							{"Hydroelectricity":"electricity generated by hydropower; the production of electrical power thorugh the use of the garviational forece of afalling or flowing water."}
							],
						"I": [
							{"Innovation":"the process of translating an idea or invention into a good or service that creates value or for which customers will pay"},
							{"Institution":"a society or organization founded for a religious, educational, social, or similar purpose."},
							{"Integration":"relationship among commitee members which is conductive to positive results rather than mere compromise."},
							{"Intelligent Electronic Device (IED)":"is used to describe microporcessor-based controllers of power system equipment, such as circuit breakers, transforemerts and capacitor banks."},
							{"Interconnection":"Is the physical linking of a carrier's network with equipment or facilitites not belonging to that network."},
							{"Interdisciplinary":"Interactive process where team members work jointly, each from his or her own discipline-specific perspective to address a common research problem."},
							{"Intergeneration relations":"are the social and family relationships between memebers of different generations."},
							{"Irradiance":"is the radiant flux (power) received by a surface per unit area"}
							],
						"K": [
							{"Kinetic energy":"is the energy that an object possesses due to its motion"}
							],
						"M": [
							{"Market":"an area or arena in which commercial dealings are conducted"},
							{"Mechanical energy":"is the sum of kinetic and potential energy, is the energy associated to the motion and position of an object"},
							{"Multidisciplinary":"a sequential process in which scholars from disparate fields work independently, each from his or her own discipline-specific perspective, periodically coming together to combine efforts to address a common research problem."}
							],
						"N": [
							{"Network":"a pattern of interdependence among social actors in which at least a portion of the links are framed in terms of something other than superior-subornidate relations."},
							{"Networks":"structures of interdependence involving multiple organizations or parts thereof, where one unit is not merely the formal subordinate of the others in some larger hierarchical management capacity is an ability to: anticipate and influence change; make informed and intelligent policy decisions; attract, absorb, and manage resources; and evaluate current activities in order to guide future action."}
							],
						"O": [
							{"Ocean current":"is the movement of seawater caused by breaking wind, waves, and salinity differences."},
							{"Ocean Thermal Energy Conversion (OTEC)":"is a marine renewable energy technology that catches the solar energy absorbed by the oceans."},
							{"Ocean tides":"are the rise and fall of sea levels cased by the combined effects of gravitational forces exerted by the Moon, Sun, and rotation of the Earth."},
							{"Ocean waves":"is a disturbance in the ocean that transmits energy from one place to another"},
							{"Open access":"refers to online research outputs that are free of all restrictions on access and free of many restrictions on use"},
							{"Organizational behavior":"is the study of the way people interact withing groups. Normally this study is applied in an attempt to create more efficient business organizations"}
							],
						"P": [
							{"Participation":"the action of taking aprt in something"},
							{"Pipeline":"is a set of data processing elements connected in series, where the output of one element is the input of the next one"},
							{"Policy":"is a deliberate system of principles to guide decisions and achieve rational outcomes"},
							{"Potential energy":"is the neergy that an object has due to its position in a force field or that a system has due to the configuration of its parts."},
							{"Power flow study":"is a numerical analysis of the flow of electric power in an interconnected system."}
							],
						"R": [
							{"Real time deployment":"structures of interdependence involving multiple organizations or parts thereof, where one unit is not merely the formal subordinate of the others in some larger hierarchical management capacity is an ability to: anticipate and influence change; make informed and intelligent policy decisions; attract, absorb, and manage resources; and evaluate current activities in order to guide future action."},
							{"Redundancy":"the duplication of critical components or functions of a system with the intention of increasing reliability"},
							{"Reputation systems":"computes and publishes reputation scores for a set of objects withing a community or domain, based on a colection of opinions that other entities hold about the objects."},
							{"Resilience":"structures of interdependence involving multiple organizations or parts thereof, where one unit is not merely the formal subordinate of the others in some larger hierarchical management capacity is an ability to: anticipate and influence change; make informed and intelligent policy decisions; attract, absorb, and manage resources; and evaluate current activities in order to guide future action."}
							],
						"S": [
							{"Scarcity":"the state of being scarce or in short supply; shortage"},
							{"Schumpeter's waves":"is an economic theory about innovation cyvles and/or technological changes."},
							{"Simulation":"is the imitation of the operation of a real-world process or system over time."},
							{"Smart appliance":"is an appliance that amy be configured to communicate information directly to the utility operator for efficient and more productive use of electricity"},
							{"Smart energy systems":"is a 100% renewable energy system that is affordable and consumes sustainable bionergy and uses its sysnergies for more efficiency."},
							{"Smart grid":"an electricity supply network that uses digital communications technology to detect and react to local changes in usage"},
							{"Smart metering technology":"refer to the information and communication technology working in balance with the power generation and consumption, allowing bidirectional transfer of information between components."},
							{"Smart meters":"is an electronic device that records consumption of electric energy in intervals of an hour or less and communicates that information at least daily back to the utility for monitoring and billing."},
							{"Social justice":"is the fair and just relation between the indicidual and society."},
							{"Sustainability":"is the endurance of systems and processes"},
							{"Social networks":"a dedicated website or other application that enables users to communicate with each other"},
							{"Social planning":"understanding and preparing for the societal outcomes of energy transitions, as well as developing strategies to incorporate these considerations into energy policy"},
							{"Social planning for energy transitions":"is an electronic device that records consumption of electric energy in intervals of an hour or less and communicates that information at least daily back to the utility for monitoring and billing."},
							{"Social preferences":"includes interpersonal altruism, fairness, reciprocity, and inequity aversion"},
							{"Sociology of Energy":"is playing a key role in shaping the academic and policy debates around a range of energy issues at every scale: from domestic heating and household energy use, to community energy projects, to urban energy governance, and huge offshore wind farms."},
							{"Sociotechnological systems":"systems that so fully intertwine social and technological elements that the two are difficult if not impossible to disentangle."},
							{"Solar winds":"is a stream of charged particles released from the upper atmosphere of the Sun."},
							{"Spark":"Apache Spark is an open source processing engine built around speed, ease of user, and analytics."},
							{"Stakeholders":"are creditors, directors, employees, government agencies, owners, suppliers, unions, and the community form which the business draws its resources."},
							{"Static algorithm":"an algorithm whose operation is known in advance. Also know as deterministic algorithm."},
							{"Strategic Niche Management (SNM)":"is a tool to support the societal introduction of radical sustainable innovations."},
							{"Streaming Algorithms":"are algorithms for processing data streams in which the input is presented as a sequence of items and can be examined in only a few passes."},
							{"Sustainable Energy Market":"is a virtual platform that gathers all renewable energy actors' expertise and work to pursue the deployment of renewable energies in developing countries."},
							{"System Restoration":"systems that so fully intertwine social and technological elements that the two are difficult if not impossible to disentangle."}
							],
						"T": [
							{"Technology Acceptance Model (TAM)":"model used in research about information systems and information technology with good predicted value"},
							{"Technology assesment":"the evaluation of an object, function, or sequence of functions – created by human society to assist in achieving a goal- with respect to sustainability in comparison of other solutions providing the same functions."},
							{"Thermal energy":"is the energy that comes from heat. The heat is generated by movement"},
							{"Tidal power":"is a form of hydropower that converts the energy obtained from tides into useful forms of power, mainly electricity."},
							{"Tolerance":"an allowable amount of variation of a specidied quantity, especially in the dimensions of a machine or part."},
							{"Tragedy of the Commons":"is a situation where individuals acting independently and rationally according to their own self-interest behave contrary to the best interests of the whole by depleting some common resource."},
							{"Transdisciplinarity":"the different perspectives of experts and stakeholders on the aspects of sustainability are essential for the design stage. Thereby, technology designers can acquire a practical integrated understanding of the most important aspects and obtain agreement on the most important performance indicators for a type of technological intervention."},
							{"Transdisciplinary":"integrative process in which researchers work jointly to develop and use a shared conceptual framework that synthesizes and extends discipline-specific theories, concepts, methods, or all three to create new models and language to address a common research problem."}
							],
						"U": [
							{"Unidisciplinary":"a process in which researchers from a single discipline work together to address a common research problem"},
							{"User":"a person who uses or operates something, especially a computer or other machine"},
							],
						"W": [
							{"Wind":"is the movement of air caused by the irrefular heating on Earth's surface."},
							{"Wind Power":"is the transformation of wind energy into more utile forms, electricity using wind turbine."},
							{"Wind Turbine":"is a machine that converts the kinetic energy from the wind into mechanical energy."}
							]
						})



