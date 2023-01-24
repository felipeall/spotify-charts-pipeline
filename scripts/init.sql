CREATE TABLE charts (
	uri text NOT NULL,
	alias text NOT NULL,
	"entityType" text NOT NULL,
	"readableTitle" text NOT NULL,
	"backgroundColor" text NOT NULL,
	"textColor" text NOT NULL,
	"latestDate" date NOT NULL,
	"earliestDate" date NOT NULL,
	country text NOT NULL,
	"chartType" text NOT NULL,
	recurrence text NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT charts_pk PRIMARY KEY (uri)
);

CREATE TABLE artists (
	"uri" text NOT NULL,
	"name" text NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT artists_pk PRIMARY KEY ("uri")
);

CREATE TABLE tracks (
	"trackName" text NOT NULL,
	"trackUri" text NOT NULL,
	"displayImageUri" text NOT NULL,
	"artistUri" _text NOT NULL,
	labels _text NOT NULL,
	"releaseDate" date NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT tracks_pk PRIMARY KEY ("trackUri")
);

CREATE TABLE ranks (
	"chartUri" text NOT NULL,
	"date" date NOT NULL,
	"trackUri" text NOT NULL,
	"currentRank" int8 NOT NULL,
	"previousRank" int8 NOT NULL,
	"peakRank" int8 NOT NULL,
	"appearancesOnChart" int8 NOT NULL,
	"consecutiveAppearancesOnChart" int8 NOT NULL,
	"metricValue" int8 NOT NULL,
	"metricType" text NOT NULL,
	"entryStatus" text NOT NULL,
	"peakDate" date NOT NULL,
	"entryRank" int8 NOT NULL,
	"entryDate" date NOT NULL,
	created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT ranks_pk PRIMARY KEY ("chartUri", "date", "currentRank")
);
