-- CreateTable
CREATE TABLE "WebPage" (
    "id" SERIAL NOT NULL,
    "url" TEXT NOT NULL,
    "text" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "classification" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "WebPage_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Summary" (
    "id" SERIAL NOT NULL,
    "webPageId" INTEGER NOT NULL,
    "summary" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Summary_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "GeneratedFunSentence" (
    "id" SERIAL NOT NULL,
    "summaryId" INTEGER NOT NULL,
    "sentence" TEXT NOT NULL,
    "mediaType" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "GeneratedFunSentence_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Video" (
    "id" SERIAL NOT NULL,
    "generatedSentenceId" INTEGER NOT NULL,
    "videoUrl" TEXT NOT NULL,
    "audioFileUrl" TEXT NOT NULL,
    "clipFileUrl" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Video_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Song" (
    "id" SERIAL NOT NULL,
    "generatedSentenceId" INTEGER NOT NULL,
    "songFileUrl" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Song_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AnimeCharacterAudio" (
    "id" SERIAL NOT NULL,
    "characterName" TEXT NOT NULL,
    "audioFileUrl" TEXT NOT NULL,
    "clipFileUrl" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "AnimeCharacterAudio_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "WebPage_url_key" ON "WebPage"("url");

-- AddForeignKey
ALTER TABLE "Summary" ADD CONSTRAINT "Summary_webPageId_fkey" FOREIGN KEY ("webPageId") REFERENCES "WebPage"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "GeneratedFunSentence" ADD CONSTRAINT "GeneratedFunSentence_summaryId_fkey" FOREIGN KEY ("summaryId") REFERENCES "Summary"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Video" ADD CONSTRAINT "Video_generatedSentenceId_fkey" FOREIGN KEY ("generatedSentenceId") REFERENCES "GeneratedFunSentence"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Song" ADD CONSTRAINT "Song_generatedSentenceId_fkey" FOREIGN KEY ("generatedSentenceId") REFERENCES "GeneratedFunSentence"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
