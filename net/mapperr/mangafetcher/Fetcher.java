package net.mapperr.mangafetcher;

public interface Fetcher
{
	public void fetch();
	public void fetchVolume(String volume);
	public void fetchChapter(String volume, String chapter);
	public void fetchPage(String name, String volume, String chapter, String page);
}
