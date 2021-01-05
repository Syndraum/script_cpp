> :warning: **Important note: still in development. Some bugs may appear**

## Presentation

Two actions as possible

`class.py className [...]` create .cpp and .hpp files. You can specify as many class names as you want

`class.sh className [...]` same as `class.py` but in shell

`update.py [...]` check .cpp and .hpp files in actual dir and generate only necessary setter and getter. You can specify class name in arguments for specific application.

`getSet.sh [...]` same as `update.py` but in shell :warning: this function do not check duplicate setter and getter

## Utilisation

run command with bash `bash ./class.sh`
or python3 `python3 ./class.py`

1. Create class

```
python3 ./class.py Personnage
```

That will create 2 files, Personnage.hpp
```cpp
#include "Personnage.hpp"

Personnage::Personnage()
{
	
}

Personnage::~Personnage()
{
	
}
```
and Personnage.cpp
```cpp
#ifndef PERSONNAGE
#define PERSONNAGE

class Personnage
{
	public:

	Personnage();
	~Personnage();
};

#endif

```

2. Insert attributes you want
```cpp
class Personnage
{
	int	mana;

	int test;
	public:

	int life;

	Personnage();
	~Personnage();

	private:

	char *name;
};
```
> :warning: Only privates attributes will be considered

3. launch update
```
python3 ./update.py
```
4. Look at the results
```cpp
class Personnage
{
	int	mana;

	int test;
	public:

	int life;

	Personnage();
	~Personnage();

	int		getMana();
	void	setMana(int mana);
	int		getTest();
	void	setTest(int test);
	char	*getName();
	void	setName(char *name);

	private:

	char *name;
};
```
```cpp
int		Personnage::getMana()
{
	return this->mana;
}

void	Personnage::setMana(int mana)
{
	this->mana = mana;
}

int		Personnage::getTest()
{
	return this->test;
}

void	Personnage::setTest(int test)
{
	this->test = test;
}

char	*Personnage::getName()
{
	return this->name;
}

void	Personnage::setName(char *name)
{
	this->name = name;
}
```
